import time

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from ykush import Ykush
from sdwire import Sdwire

# The builder is a "configuration" of the U-Boot build for this board.  In its
# simplest form you just need to configure the defconfig and toolchain which
# should be used.
class Rpi3UBootBuilder(uboot.UBootBuilder):
    name = "rpi_3"
    # Is this the correct defconfig?
    defconfig = "rpi_3_32b_defconfig"
    # As defined in the lab-config (kea.py)
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

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.sdwire_dut()
        self.ykush_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.ykush_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port1")

    def flash(self, repo: git.GitRepository) -> None:
        board = self
        host = self.host
        #pp = pprint.PrettyPrinter()
        #pp.pprint(self.__dict__)
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
        #host.exec0(repo / "u-boot.bin", "%s/rpi3-u-boot.bin" % self.mount_point)

        print("host", self.host)
        print("repo", repo / "fred")

        host.exec0("umount", "UUID=%s" % self.mount_uuid)

        board.sdwire_dut()

# Not sure if this the correct config for this boards U-Boot ... It does not
# matter if you just care about building U-Boot though.
class Rpi3UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "

    build = Rpi3UBootBuilder()

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class Rpi3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    # Username for logging in once linux has booted
    username = "pi"
    # Password.  If you don't need a password, set this to `None`
    password = "raspberry"

# tbot will check for `BOARD`, don't forget to set it!
BOARD = Rpi3
UBOOT = Rpi3UBoot
# You need to set `LINUX` now as well.
LINUX = Rpi3Linux
