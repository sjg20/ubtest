import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from dli import Dli
from sdwire import Sdwire

class Opi_PcUBootBuilder(uboot.UBootBuilder):
    name = "opi_pc"
    defconfig = "orangepi_pc_defconfig"
    toolchain = "armv7-a"

class Opi_Pc(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Dli,
    Sdwire,
):
    name = "opi_pc"
    desc = "Orange Pi PC"
    console_uart = "/dev/ttyusb_port4"
    dli_hostname = "192.168.4.19"
    dli_outlet = 1
    dli_password = "1234"
    dli_user = "admin"
    raw_device = "/dev/sdcard1"
    sdwire_serial = "202001064004"

    ether_mac = "None"

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.dli_on()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.dli_off()
        self.sdwire_ts()
        self.flash_sunxi(repo)
        self.sdwire_dut()


class Opi_PcUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Opi_PcUBootBuilder()


class Opi_PcLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "None"
    password = "None"


BOARD = Opi_Pc
UBOOT = Opi_PcUBoot
LINUX = Opi_PcLinux
