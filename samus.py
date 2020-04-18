import os
import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from chromebook import Chromebook, ChromebookLinux

class SamusUBootBuilder(uboot.UBootBuilder):
    name = "samus"
    defconfig = "chromebook_samus_defconfig"
    toolchain = "i386"

    def do_patch(self, repo: git.GitRepository) -> None:
        #shell.copy(self.host.fsroot / "/vid/software/devel/link/*.bin",
                   #path / "board/google/chromebook_link")
        bindir = os.path.join(repo._local_str(),
                              "board/google/chromebook_samus")
        repo.host.exec0("bash", "-c",
                        "cp /vid/software/devel/samus/bin/*.bin %s" % bindir)

class Samus(
    Chromebook
):
    name = "Samus"
    servo_name = "samus"

    ether_mac = "?"
    em100_chip = "W25Q64CV"
    em100_serial = "DP033694"

    def flash(self, repo: git.GitRepository) -> None:
        rom_fname = os.path.join(repo._local_str(), "u-boot.rom")
        self.host.exec0("em100", "-x", self.em100_serial, "-s", "-p", "LOW",
                        "-c", self.em100_chip, "-d", rom_fname, "-r")


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
    username = "None"
    password = "None"


BOARD = Samus
UBOOT = SamusUBoot
LINUX = SamusLinux
