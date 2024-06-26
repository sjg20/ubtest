# Generated by labman from dut pine64

import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from send import Send
from blobs import Blobs
from sdwire import Sdwire
from usbrelay import Usbrelay

class Pine64UBootBuilder(uboot.UBootBuilder, Blobs):
    name = "pine64"
    defconfig = "pine64_plus_defconfig"
    toolchain = "aarch64"
    blob_dest = "."
    blob_src = "/vid/software/devel/pine/bl31.bin"

    def do_patch(self, repo: git.GitRepository) -> None:
        self.add_blobs(repo)


class Pine64(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Send,
    Sdwire,
    Usbrelay,
):
    name = "pine64"
    desc = "Pine A64 Plus 2GB"
    block_device = "/dev/sdcard11"
    console_uart = "/dev/ttyusb_port22"
    sdwire_serial = "da63"
    send_device = "/dev/usbdev-pinea64"
    usbboot_loadaddr = 0x4a000000
    usbboot_port = "1-2.2.1"
    usbrelay_name = "7QMBS"
    usbrelay_reset = "4"

    ether_mac = None

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.usbrelay_toggle_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200", self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.flash_sunxi(repo)
        self.sdwire_dut()

    def send(self, repo: git.GitRepository) -> None:
        self.sdwire_ts()
        self.send_sunxi(repo)
        self.sdwire_dut()


class Pine64UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Pine64UBootBuilder()


class Pine64Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Pine64
UBOOT = Pine64UBoot
LINUX = Pine64Linux
