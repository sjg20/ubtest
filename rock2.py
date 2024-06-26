# Generated by labman from dut rock2

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from sdwire import Sdwire
from ykush import Ykush

class Rock2UBootBuilder(uboot.UBootBuilder):
    name = "rock2"
    defconfig = "rock2_defconfig"
    toolchain = "armv7-a"

class Rock2(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Sdwire,
    Ykush,
):
    name = "rock2"
    desc = "Rock 2"
    block_device = "/dev/sdcard3"
    console_uart = "/dev/ttyusb_port8"
    sdwire_serial = "sdwireda10"
    ykush_port = "3"
    ykush_serial = "YK17698"

    ether_mac = "02:4f:04:03:26:d1"

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
        self.flash_rockchip(repo)
        self.sdwire_dut()

    def send(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.ykush_reset()
        self.send_None(repo)
        self.sdwire_dut()


class Rock2UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Rock2UBootBuilder()


class Rock2Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Rock2
UBOOT = Rock2UBoot
LINUX = Rock2Linux
