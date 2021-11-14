import os
import re
import tempfile
import time

import tbot
from tbot.log import Verbosity
from tbot.tc import shell

class Send:
    def wait_for_send_device(self):
        tbot.log.EventIO(None, "Wait for board (%s)" % self.name,
                         verbosity=Verbosity.QUIET)
        done = False
        for i in range(10):
            try:
                self.host.exec0("ls", self.send_device)
                done = True
                if done:
                    break
            except Exception as e:
                pass
            time.sleep(1)
        if not done:
            raise ValueError("Cannot access device '%s'" % self.send_device)

    def find_bus_device(self):
        cmd = ['readlink', self.send_device]
        out = self.host.exec0(*cmd)

        regex = re.compile('bus/usb/(\d{3})/(\d{3})')
        m = regex.search(out)
        if not m:
            raise ValueError("Cannot find device USB bus/dev in '%s'" % out)
        bus = m.group(1)
        device = m.group(2)
        return bus, device

    def send_tegra(self, repo):
        self.wait_for_send_device()

        tbot.log.EventIO(None, "Send U-Boot (%s)" % self.name,
                         verbosity=Verbosity.QUIET)
        u_boot = os.path.join(repo._local_str(), "u-boot-dtb-tegra.bin")
        cmd = ['tegrarcm', '--bct=' + self.tegra_bct,
               '--bootloader=%s' % u_boot ,
               '--loadaddr=%#08x' % self.usbboot_loadaddr,
               '--usb-port-path', self.usbboot_port]
        self.host.exec0(*cmd)

    def send_sunxi(self, repo):
        self.wait_for_send_device()
        cmd = ['readlink', self.send_device]
        out = self.host.exec0(*cmd)

        bus, device = self.find_bus_device()

        tbot.log.EventIO(None, "Send SPL (%s)" % self.name,
                         verbosity=Verbosity.QUIET)
        args = ['-d', '%s:%s' % (bus, device)]
        spl = os.path.join(repo._local_str(), "spl/sunxi-spl.bin")
        cmd = ['sunxi-fel'] + args + ['spl', spl]
        self.host.exec0(*cmd)

        tbot.log.EventIO(None, "Send U-Boot (%s)" % self.name,
                         verbosity=Verbosity.QUIET)
        uboot = os.path.join(repo._local_str(), "u-boot.bin")
        cmd = ['sunxi-fel'] + args + ['write', '%#x' % self.usbboot_loadaddr,
                                      uboot]
        self.host.exec0(*cmd)

        cmd = ['sunxi-fel'] + args + ['exe', '%#x' % self.usbboot_loadaddr]
        self.host.exec0(*cmd)

    def send_imx(self, repo):
        self.wait_for_send_device()
        with tbot.acquire_local() as lo, \
              tempfile.TemporaryDirectory() as tmpdir:
            main = 'imx_usb.conf'
            rom = 'mx6_usb_rom.conf'
            spl = 'mx6_usb_sdp_spl.conf'
            tmp = 'imx_loader_tmp'

            #main_fname = os.path.join(tmpdir, 'imx_usb.conf')
            main_fname = lo.fsroot / tmpdir / 'imx_usb.conf'
            with open(main_fname._local_str(), 'w') as fd:
                print('0x15a2:0x0054, %s, 0x0525:0xb4a4, %s' % (rom, spl),
                      file=fd)

            rom_fname = lo.fsroot / tmpdir / rom
            with open(rom_fname._local_str(), 'w') as fd:
                print('''mx6_qsb
hid,1024,0x910000,0x10000000,1G,0x00900000,0x40000
SPL:jump header2
''', file=fd)

            spl_fname = lo.fsroot / tmpdir / spl
            with open(spl_fname._local_str(), 'w') as fd:
                print('''mx6_spl_sdp
#hid/bulk,[old_header,]max packet size, {ram start, ram size}(repeat valid ram areas\
)
#In SPL, we typically load u-boot.img which has a U-boot header...
hid,uboot_header,1024,0x10000000,1G,0x00907000,0x31000
%s/u-boot.img:load 0x177fffc0,jump 0x17800000
''' % repo._local_str(), file=fd)

            self.host.exec0('mkdir', '-p', repo / tmp)
            shell.copy(main_fname, repo / tmp / main)
            shell.copy(rom_fname, repo / tmp / rom)
            shell.copy(spl_fname, repo / tmp / spl)
        bus, device = self.find_bus_device()

        tbot.log.EventIO(None, "Send SPL (%s)" % self.name,
                         verbosity=Verbosity.QUIET)
        args = ['-b', bus, '-D', device]
        cmd = ['cd', repo._local_str(), ';', 'imx_usb'] + args
        cmd += ['-c', tmp]
        self.host.exec0('bash', '-c', ' '.join(cmd))

    def samsung_usbdl(self, addr, fname):
        bus, device = self.find_bus_device()
        cmd = ["smdk-usbdl", "-a", '%x' % addr, '-b', bus, '-d', device,
               '-f', fname]
        self.host.exec0(*cmd)

    def send_samsung(self, repo):
        self.wait_for_send_device()
        time.sleep(0.5)
        self.samsung_usbdl(self.usbboot_loadaddr,
                      '/vid/software/devel/exynos/snow/u-boot.bl1.bin')

        # CONFIG_SPL_TEXT_BASE 0x02023400
        spl_text_base = 0x02023400
        spl = os.path.join(repo._local_str(), "spl/u-boot-spl.bin")
        self.samsung_usbdl(spl_text_base, spl)

        # CONFIG_SYS_TEXT_BASE 0x43E00000
        spl_text_base = 0x43e00000
        spl = os.path.join(repo._local_str(), "u-boot.bin")
        self.samsung_usbdl(spl_text_base, spl)

    def send_rockchip(self, repo):
        """Send to Rockchip SoC over USB

        http://opensource.rock-chips.com/wiki_Rockusb
        """
        self.wait_for_send_device()
