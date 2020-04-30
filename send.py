import os
import re
import time

from tbot.tc import shell

class Send:
    def wait_for_device(self, device):
        done = False
        for i in range(10):
            try:
                self.host.exec0("ls", device)
                done = True
                if done:
                    break
            except Exception as e:
                pass
            time.sleep(1)
        if not done:
            raise ValueError("Cannot access device '%s'" % device)

    def send_tegra(self, repo):
        self.wait_for_device(self.tegra_device)
        u_boot = os.path.join(repo._local_str(), "u-boot-dtb-tegra.bin")
        cmd = ['tegrarcm', '--bct=' + self.tegra_bct,
               '--bootloader=%s' % u_boot ,
               '--loadaddr=0x%08x' % self.tegra_loadaddr,
               '--usb-port-path', self.tegra_port]
        self.host.exec0(*cmd)

    def send_sunxi(self, repo):
        self.wait_for_device(self.sunxi_device)
        cmd = ['readlink', self.sunxi_device]
        out = self.host.exec0(*cmd)
        print('out', out)

        regex = re.compile('bus/usb/(\d{3})/(\d{3})')
        m = regex.search(out)
        if not m:
            raise ValueError("Cannot find device USB bus/dev in '%s'" % out)
        bus = m.group(1)
        device = m.group(2)

        args = ['-d', '%s:%s' % (bus, device)]
        spl = os.path.join(repo._local_str(), "spl/sunxi-spl.bin")
        cmd = ['sunxi-fel'] + args + ['spl', spl]
        self.host.exec0(*cmd)

        uboot = os.path.join(repo._local_str(), "u-boot.bin")
        cmd = ['sunxi-fel'] + args + ['write', '0x4a000000', uboot]
        self.host.exec0(*cmd)

        cmd = ['sunxi-fel'] + args + ['exe', '0x4a000000']
        self.host.exec0(*cmd)

#/dev/bus/usb/004/047
