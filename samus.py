# Generated by labman from dut samus

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from blobs import Blobs
from servo import Servo

class SamusUBootBuilder(uboot.UBootBuilder, Blobs):
    name = "samus"
    defconfig = "chromebook_samus_defconfig"
    toolchain = "i386"
    blob_dest = "board/google/chromebook_samus"
    blob_src = "/vid/software/devel/samus/bin/*.bin"

    def do_patch(self, repo: git.GitRepository) -> None:
        self.add_blobs(repo)


class Samus(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Servo,
):
    name = "samus"
    desc = "Chromebook Pixel 2"
    em100_chip = "W25Q64CV"
    em100_serial = "DP025143"
    servo_port = 9900

    ether_mac = None

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.servo_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        pass

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        self.console_uart = self.servo_get_tty()
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.flash_em100(repo)


class SamusUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = SamusUBootBuilder()


class SamusLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "root"
    password = "test0000"


BOARD = Samus
UBOOT = SamusUBoot
LINUX = SamusLinux
