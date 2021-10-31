# Generated by labman from dut puma

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from dli import Dli
from sdwire import Sdwire
from usbrelay import Usbrelay

class PumaUBootBuilder(uboot.UBootBuilder):
    name = "puma"
    defconfig = "puma-rk3399_defconfig"
    toolchain = "aarch64"

class Puma(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Dli,
    Sdwire,
    Usbrelay,
):
    name = "puma"
    desc = "Theobroma Systems Puma RK3399"
    console_uart = "/dev/ttyusb_port6"
    dli_hostname = "192.168.4.19"
    dli_outlet = "2"
    dli_password = "1234"
    dli_user = "admin"
    sdwire_serial = "202001064005"
    usbrelay_name = "6QMBS"
    usbrelay_power_button = "8"
    usbrelay_reset = "7"

    ether_mac = None

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.dli_reset()
        self.usbrelay_toggle_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200", self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.flash_rockchip(repo)
        self.sdwire_dut()


class PumaUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = PumaUBootBuilder()


class PumaLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Puma
UBOOT = PumaUBoot
LINUX = PumaLinux
