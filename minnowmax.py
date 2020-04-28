import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from blobs import Blobs
from dli import Dli

class MinnowmaxUBootBuilder(uboot.UBootBuilder, Blobs):
    name = "minnowmax"
    defconfig = "minnowmax_defconfig"
    toolchain = "i386"
    blob_dest = "board/intel/minnowmax"
    blob_src = "/vid/software/devel/minnowmax/bin/*.bin"

    def do_patch(self, repo: git.GitRepository) -> None:
        self.add_blobs(repo)


class Minnowmax(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Dli,
):
    name = "minnowmax"
    desc = "Minnowboard Max"
    console_uart = "/dev/ttyusb_port7"
    dli_hostname = "192.168.4.19"
    dli_outlet = 6
    dli_password = "1234"
    dli_user = "admin"
    em100_chip = "W25Q64DW"
    em100_serial = "DP139140"

    ether_mac = "None"

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.dli_on()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.dli_off()
        
        self.flash_em100(repo)
        


class MinnowmaxUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = MinnowmaxUBootBuilder()


class MinnowmaxLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "None"
    password = "None"


BOARD = Minnowmax
UBOOT = MinnowmaxUBoot
LINUX = MinnowmaxLinux
