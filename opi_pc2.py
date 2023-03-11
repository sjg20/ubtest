# Generated by labman from dut opi_pc2

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from dli import Dli
from sdwire import Sdwire

class Opi_Pc2UBootBuilder(uboot.UBootBuilder):
    name = "opi_pc2"
    defconfig = "orangepi_pc2_defconfig"
    toolchain = "aarch64"

class Opi_Pc2(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Dli,
    Sdwire,
):
    name = "opi_pc2"
    desc = "Orange Pi PC 2"
    block_device = "/dev/sdcard6"
    console_uart = "/dev/ttyusb_port14"
    dli_hostname = "192.168.4.19"
    dli_outlet = "8"
    dli_password = "1234"
    dli_user = "admin"
    sdwire_serial = "sdwireda3"
    send_device = "/dev/usbdev-opi_pc2"
    usbboot_loadaddr = 0x4a000000
    usbboot_port = "4-10.4.3"

    ether_mac = None

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.dli_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.flash_sunxi(repo)
        self.sdwire_dut()

    def send(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.dli_reset()
        self.send_sunxi(repo)
        self.sdwire_dut()


class Opi_Pc2UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Opi_Pc2UBootBuilder()


class Opi_Pc2Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Opi_Pc2
UBOOT = Opi_Pc2UBoot
LINUX = Opi_Pc2Linux
