import os
import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from chromebook import Chromebook, ChromebookLinux

# The builder is a "configuration" of the U-Boot build for this board.  In its
# simplest form you just need to configure the defconfig and toolchain which
# should be used.
class SamusUBootBuilder(uboot.UBootBuilder):
    name = "samus"
    # Is this the correct defconfig?
    defconfig = "chromebook_samus_defconfig"
    # As defined in the lab-config (kea.py)
    toolchain = "i386"


class Samus(
    Chromebook
):
    name = "Samus"
    servo_name = "samus"

    ether_mac = "?"
    em100_chip = "W25Q64CV"
    em100_serial = "DP033694"

    def add_blobs(self, path: linux.Path) -> None:
        #shell.copy(self.host.fsroot / "/vid/software/devel/link/*.bin",
                   #path / "board/google/chromebook_link")
        bindir = os.path.join(path._local_str(), "board/google/chromebook_samus")
        self.host.exec0("bash", "-c",
                        "cp /vid/software/devel/samus/bin/*.bin %s" % bindir)

    def flash(self, repo: git.GitRepository) -> None:
        rom_fname = os.path.join(repo._local_str(), "u-boot.rom")
        self.host.exec0("em100", "-x", self.em100_serial, "-s", "-p", "LOW",
                        "-c", self.em100_chip, "-d", rom_fname, "-r")


# Not sure if this the correct config for this boards U-Boot ... It does not
# matter if you just care about building U-Boot though.
class SamusUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "

    build = SamusUBootBuilder()


# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class SamusLinux(
    ChromebookLinux
):
    # Username for logging in once linux has booted
    username = "root"
    # Password.  If you don't need a password, set this to `None`
    password = "test0000"


# tbot will check for `BOARD`, don't forget to set it!
BOARD = Samus
UBOOT = SamusUBoot
# You need to set `LINUX` now as well.
LINUX = SamusLinux
