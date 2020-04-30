# Generated by labman from dut opi_pc

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
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
    Send,
    Dli,
    Sdwire,
):
    name = "opi_pc"
    desc = "Orange Pi PC"
    block_device = "/dev/sdcard1"
    console_uart = "/dev/ttyusb_port4"
    dli_hostname = "192.168.4.19"
    dli_outlet = "1"
    dli_password = "1234"
    dli_user = "admin"
    sdwire_serial = "202001064004"
    send_device = "/dev/usbdev-opi-pc"
    usbboot_loadaddr = 0x4a000000
    usbboot_port = "6-2.1.3"

    ether_mac = "02:81:d5:d8:6c:39"

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
    username = ""
    password = ""


BOARD = Opi_Pc
UBOOT = Opi_PcUBoot
LINUX = Opi_PcLinux
