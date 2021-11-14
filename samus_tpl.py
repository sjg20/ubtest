# Generated by labman from dut samus_tpl

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from blobs import Blobs
from dli import Dli
from servo import Servo

class Samus_TplUBootBuilder(uboot.UBootBuilder, Blobs):
    name = "samus_tpl"
    defconfig = "chromebook_samus_tpl_defconfig"
    toolchain = "i386"
    blob_dest = "board/google/chromebook_samus"
    blob_src = "/vid/software/devel/samus/bin/*.bin"

    def do_patch(self, repo: git.GitRepository) -> None:
        self.add_blobs(repo)


class Samus_Tpl(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Dli,
    Servo,
):
    name = "samus_tpl"
    desc = "Chromebook Pixel 2 (TPL)"
    dli_hostname = "192.168.4.22"
    dli_outlet = "3"
    dli_password = "1234"
    dli_user = "admin"
    em100_chip = "W25Q64CV"
    em100_serial = "DP025143"
    servo_port = 0x26ac

    ether_mac = None

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.dli_reset()
        self.servo_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        self.console_uart = self.servo_get_tty()
        return mach.open_channel("picocom", "-q", "-b", "115200", self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.flash_em100(repo)

    def send(self, repo: git.GitRepository) -> None:
        self.dli_reset()
        self.send_None(repo)


class Samus_TplUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Samus_TplUBootBuilder()


class Samus_TplLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "root"
    password = "test0000"


BOARD = Samus_Tpl
UBOOT = Samus_TplUBoot
LINUX = Samus_TplLinux