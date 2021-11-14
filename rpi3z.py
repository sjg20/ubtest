# Generated by labman from dut rpi3z

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from sdwire import Sdwire
from ykush import Ykush

class Rpi3ZUBootBuilder(uboot.UBootBuilder):
    name = "rpi3z"
    defconfig = "rpi_3_32b_defconfig"
    toolchain = "armv7-a"

class Rpi3Z(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Sdwire,
    Ykush,
):
    name = "rpi3z"
    desc = "Raspberry Pi 3b Fedora 31"
    console_uart = "/dev/ttyusb_port20"
    mount_point = "rpi3z_b_boot"
    mount_uuid = "B7F8-3D1C"
    sdwire_serial = "da61"
    ykush_port = "2"
    ykush_serial = "YK19193"

    ether_mac = "b8:27:eb:b4:f9:02"

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
        return mach.open_channel("picocom", "-q", "-b", "115200", self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.flash_rpi(repo)
        self.sdwire_dut()

    def send(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.ykush_reset()
        self.send_None(repo)
        self.sdwire_dut()


class Rpi3ZUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "U-Boot> "
    build = Rpi3ZUBootBuilder()


class Rpi3ZLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "pi"
    password = "raspberry"


BOARD = Rpi3Z
UBOOT = Rpi3ZUBoot
LINUX = Rpi3ZLinux