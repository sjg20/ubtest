# Generated by labman from dut edison

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from dli import Dli
from usbrelay import Usbrelay

class EdisonUBootBuilder(uboot.UBootBuilder):
    name = "edison"
    defconfig = "edison_defconfig"
    toolchain = "i385"

class Edison(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Dli,
    Usbrelay,
):
    name = "edison"
    desc = "Intel Edison"
    console_uart = "/dev/ttyusb_port17"
    dli_hostname = "192.168.4.22"
    dli_outlet = "5"
    dli_password = "1234"
    dli_user = "admin"
    send_device = "/dev/usbdev-edison"
    usbboot_loadaddr = None
    usbboot_port = "4-10.1.3.1"
    usbrelay_name = "7QMBS"
    usbrelay_recovery = "6"
    usbrelay_reset = "5"

    ether_mac = None

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.dli_reset()
        self.usbrelay_toggle_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        self.dli_on()
        #self.wait_for_uart(0.7)
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.flash_edison(repo)

    def send(self, repo: git.GitRepository) -> None:
        self.dli_reset()
        self.send_edison(repo)


class EdisonUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = EdisonUBootBuilder()


class EdisonLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Edison
UBOOT = EdisonUBoot
LINUX = EdisonLinux