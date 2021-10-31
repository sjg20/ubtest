import os
import time

from tbot.tc import shell

class Flash:
    def wait_for_block_device(self):
        done = False
        for i in range(10):
            try:
                self.host.exec0("dd", "if=%s" % self.block_device,
                                "of=/dev/null", "count=1")
                done = True
                if done:
                    break
            except Exception as e:
                pass
            time.sleep(1)
        if not done:
            raise ValueError("Cannot access device '%s'" % self.block_device)

    def wait_for_mount(self):
        host = self.host
        done = False
        for i in range(5):
            out = ""
            try:
                retcode, out = host.exec("mount", "UUID=%s" % self.mount_uuid)
                done = retcode == 0
                if done:
                    break
            except Exception as e:
                pass
            if "already mounted" in out:
                # If it is already mounted, try to unmount it first. It may have
                # been mounted by another user so we won't have the access we
                # need. If this gives an error then it might be transient, e.g.
                # "Operation not permitted" is sometimes returned when there are
                # I/O errors on the device.
                host.exec("umount", "UUID=%s" % self.mount_uuid)
            time.sleep(1)
        if not done:
            raise ValueError("Cannot access mount '%s'" % self.mount_uuid)

    def dd_to_block_device(self, fname, seek, bs=512, sync=True, count=None):
        args = ["dd", "if=%s" % fname, "of=%s" % self.block_device,
                "seek=%d" % seek, "bs=%d" % bs]
        if count:
            args.append('count=%d' % count)
        self.host.exec0(*args)
        if sync:
            self.host.exec0("sync", self.block_device)

    def unmount(self):
        host = self.host
        done = False
        for i in range(5):
            try:
                retcode, out = host.exec("umount", "UUID=%s" % self.mount_uuid)
                done = retcode == 0
                if done:
                    break
            except Exception as e:
                pass
            time.sleep(1)
        if not done:
            raise ValueError("Cannot unmount '%s'" % self.mount_uuid)

    def flash_sunxi(self, repo):
        self.wait_for_block_device()
        self.dd_to_block_device('/dev/zero', 0, bs=1024, count=1024)
        host = self.host
        fname = os.path.join(repo._local_str(), "u-boot-sunxi-with-spl.bin")
        self.dd_to_block_device(fname, 8, bs=1024)

    def flash_rpi(self, repo):
        host = self.host
        self.wait_for_mount()

        # Enable the UART and fix the GPU frequency so it works correctly
        config = "/media/%s/config.txt" % self.mount_point
        host.exec0("sed", "-i", "/enable_uart/c\enable_uart = 1", config)
        retcode, _ = host.exec("grep", "-q", "^gpu_freq=250", config)
        if retcode:
            host.exec0("bash", "-c", "echo gpu_freq=250 >>%s" % config)

        # Copy U-Boot over from the build directory
        shell.copy(repo / "u-boot.bin",
                   host.fsroot / ("/media/%s/rpi3-u-boot.bin" %
                                  self.mount_point))
        self.unmount()

    def flash_rockchip(self, repo):
        self.wait_for_block_device()
        host = self.host

        #fname = os.path.join(repo._local_str(), "spl/u-boot-spl.bin")
        #tmp = os.path.join(repo._local_str(), "out.tmp")
        #host.exec0(mkimage, "-n", "rk3288", "-T", "rksd", "-d", fname, tmp)
        #self.dd_to_block_device(tmp, 64)
        fname = os.path.join(repo._local_str(), "u-boot-rockchip.bin")
        self.dd_to_block_device(fname, 64)
        #fname = os.path.join(repo._local_str(), "u-boot-dtb.img")
        #self.dd_to_block_device(fname, 16384)

    def flash_rockchip3399_tpl(self, repo):
        self.wait_for_block_device()
        host = self.host

        idb = os.path.join(repo._local_str(), "idbloader.img")
        self.dd_to_block_device(idb, 64, sync=False)
        u_boot = os.path.join(repo._local_str(), "u-boot.itb")
        self.dd_to_block_device(u_boot, 16384)

    def flash_em100(self, repo):
        rom_fname = os.path.join(repo._local_str(), "u-boot.rom")
        self.host.exec0("em100", "-x", self.em100_serial, "-s", "-p", "LOW",
                        "-c", self.em100_chip, "-d", rom_fname, "-r")

    def flash_davinci(self, repo):
        self.wait_for_block_device()
        host = self.host

        u_boot = os.path.join(repo._local_str(), "u-boot.ais")
        self.dd_to_block_device(u_boot, 117)
