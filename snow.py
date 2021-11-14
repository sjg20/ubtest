# Generated by labman from dut snow

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from dli import Dli
from servo import Servo

class SnowUBootBuilder(uboot.UBootBuilder):
    name = "snow"
    defconfig = "snow_defconfig"
    toolchain = "armv7-a"

class Snow(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Dli,
    Servo,
):
    name = "snow"
    desc = "Chromebook Snow"
    dli_hostname = "192.168.4.22"
    dli_outlet = "7"
    dli_password = "1234"
    dli_user = "admin"
    send_device = "/dev/usbdev-snow"
    servo_port = 0x26b2
    usbboot_loadaddr = 0x2021400
    usbboot_port = "1-4.2.4"

    ether_mac = "none"

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
        self.flash_None(repo)

    def send(self, repo: git.GitRepository) -> None:
        self.servo_recovery()
        self.send_samsung(repo)


class SnowUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = SnowUBootBuilder()


class SnowLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Snow
UBOOT = SnowUBoot
LINUX = SnowLinux
