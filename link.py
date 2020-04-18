import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from blobs import Blobs
from servo import Servo

class LinkUBootBuilder(uboot.UBootBuilder, Blobs):
    name = "link"
    defconfig = "chromebook_link_defconfig"
    toolchain = "i386"
    blob_dest = "board/google/chromebook_link"
    blob_src = "/vid/software/devel/link/bin/*.bin"

    def do_patch(self, repo: git.GitRepository) -> None:
        self.add_blobs(repo)


class Link(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Servo,
):
    name = "link"
    desc = "Chromebook Pixel"
    em100_chip = "W25Q64FV"
    em100_serial = "DP022781"
    servo_port = 9902

    ether_mac = "94:eb:2c:00:03:b6"

    def poweron(self) -> None:
        """Procedure to turn power on."""
        
        self.servo_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.servo_off()
        

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        self.console_uart = self.servo_get_tty()
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.servo_off()
        
        self.flash_em100(repo)
        


class LinkUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = LinkUBootBuilder()


class LinkLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "None"
    password = "None"


BOARD = Link
UBOOT = LinkUBoot
LINUX = LinkLinux
