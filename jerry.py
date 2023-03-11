# Generated by labman from dut jerry

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from servo import Servo

class JerryUBootBuilder(uboot.UBootBuilder):
    name = "jerry"
    defconfig = "chromebook_jerry_defconfig"
    toolchain = "armv7-a"

class Jerry(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Servo,
):
    name = "jerry"
    desc = "Jerry"
    em100_chip = "GD25LQ32"
    em100_serial = "DP022783"
    servo_port = 0x26af

    ether_mac = "00:1a:11:30:09:25"

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
        self.servo_reset()

    def send(self, repo: git.GitRepository) -> None:
        self.servo_reset()
        self.send_None(repo)


class JerryUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = JerryUBootBuilder()


class JerryLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "root"
    password = "test0000"


BOARD = Jerry
UBOOT = JerryUBoot
LINUX = JerryLinux
