import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from dli import Dli
from sdwire import Sdwire

class Opi_PcUBootBuilder(uboot.UBootBuilder):
    name = "opi_pc"
    defconfig = "orangepi_pc_defconfig"
    toolchain = "armv7-a"

class OrangepiPc(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Dli,
    Sdwire
):
    name = "Orange Pi PC"
    dli_hostname = "192.168.4.19"
    dli_outlet = 1
    dli_password = "1234"
    dli_user = "admin"
    sdwire_serial = "202001064004"

    #ether_mac = "02:4f:04:03:26:d1"

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
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port4")

class OrangepiPcLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""

# tbot will check for `BOARD`, don't forget to set it!
BOARD = OrangepiPc
# You need to set `LINUX` now as well.
LINUX = OrangepiPcLinux
