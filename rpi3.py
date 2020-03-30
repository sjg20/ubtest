import time

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from ykush import Ykush
from sdwire import Sdwire

class Rpi3UBootBuilder(uboot.UBootBuilder):
    name = "rpi_3"
    defconfig = "rpi_3_32b_defconfig"
    toolchain = "armv7-a"


class Rpi3(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Ykush,
    Sdwire,
):
    name = "Raspberry Pi 3b"
    ykush_serial = "YK17698"
    ykush_port = "1"

    sdwire_serial = "sdwire-18"

    ether_mac = "b8:27:eb:b4:f9:f2"

    mount_uuid = "B529-9710"
    mount_point = "rpi3_b_boot"

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.ykush_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.ykush_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port1")

    def flash(self, repo: git.GitRepository) -> None:
        board = self
        host = self.host
        board.poweroff()
        out = host.exec0("whoami")
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
            raise ValueError("Cannot access mount '%s'" % board.mount_uuid)

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

        host.exec0("umount", "UUID=%s" % self.mount_uuid)

        board.sdwire_dut()


class Rpi3UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Rpi3UBootBuilder()


class Rpi3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "pi"
    password = "raspberry"


BOARD = Rpi3
UBOOT = Rpi3UBoot
LINUX = Rpi3Linux
