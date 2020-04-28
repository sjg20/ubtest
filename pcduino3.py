
import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from sdwire import Sdwire
from ykush import Ykush

class Pcduino3UBootBuilder(uboot.UBootBuilder):
    name = "pcduino3"
    defconfig = "Linksprite_pcDuino3_defconfig"
    toolchain = "armv7-a"

class Pcduino3(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Sdwire,
    Ykush,
):
    name = "pcduino3"
    desc = "Linksprite pcDuino 3"
    console_uart = "/dev/ttyusb_port2"
    raw_device = "/dev/sdcard0"
    sdwire_serial = "sdwire-7"
    ykush_port = "2"
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

    #def power_check(self) -> bool:
        #return not self.ykush_is_on()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.ykush_off()
        self.sdwire_ts()
        self.flash_sunxi(repo)
        self.sdwire_dut()


class Pcduino3UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Pcduino3UBootBuilder()


class Pcduino3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "None"
    password = "None"


BOARD = Pcduino3
UBOOT = Pcduino3UBoot
LINUX = Pcduino3Linux
