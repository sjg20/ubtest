import os
import re
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
        bus, device = self.find_bus_device()

        tbot.log.EventIO(None, "Send SPL (%s)" % self.name,
                         verbosity=Verbosity.QUIET)
        args = ['-b', bus, '-D', device]
        spl = os.path.join(repo._local_str(), "spl/u-boot-spl.bin")
        cmd = ['imx_usb'] + args + [spl, '-l%#x' % self.usbboot_loadaddr]
        self.host.exec0(*cmd)
