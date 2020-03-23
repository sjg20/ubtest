import pprint
import socket
import time

import tbot
from tbot.machine import board, channel, connector, linux
from ykush import Ykush
from sdwire import Sdwire
from tbot.tc import git, uboot

BLK_SIZE = 1024

# The builder is a "configuration" of the U-Boot build for this board.  In its
# simplest form you just need to configure the defconfig and toolchain which
# should be used.
class Pcduino3UBootBuilder(uboot.UBootBuilder):
    name = "pcduino3"
    # Is this the correct defconfig?
    defconfig = "Linksprite_pcDuino3_defconfig"
    # As defined in the lab-config (kea.py)
    toolchain = "armv7-a"


class Pcduino3(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Ykush,
    Sdwire,
):
    name = "pcDuino3"
    ykush_serial = "YK17698"
    ykush_port = "2"

    sdwire_serial = "sdwire-7"
    raw_device = "/dev/sdcard0"

    ether_mac = "02:4f:04:03:26:d1"

    def poweron(self) -> None:
        """Procedure to turn power on."""

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.sdwire_dut()
        self.ykush_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.ykush_off()
        self.sdwire_ts()

    def power_check(self) -> bool:
        return not self.ykush_is_on()

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port2")

    def flash(self, repo: git.GitRepository) -> None:
        board = self
        host = self.host
        #pp = pprint.PrettyPrinter()
        #pp.pprint(self.__dict__)
        board.poweroff()
        done = False
        for i in range(10):
            try:
                host.exec0("dd", "if=%s" % board.raw_device, "of=/dev/null",
                           "count=1")
                done = True
                if done:
                    break
            except Exception as e:
                pass
            time.sleep(1)
        if not done:
            raise ValueError("Cannot access device '%s'" % board.raw_device)

        host.exec0("dd", "if=/dev/zero", "of=%s" % board.raw_device, "bs=1k",
                   "count=1024")
        host.exec0("dd", "if=%s" % (repo / 'u-boot-sunxi-with-spl.bin'),
                   "of=%s" % board.raw_device, "bs=1k", "seek=8")
        host.exec0("sync", board.raw_device)
        print("board.raw_device", board.raw_device)
        print("host", self.host)
        print("repo", repo / "fred")

        board.sdwire_dut()


# Not sure if this the correct config for this boards U-Boot ... It does not
# matter if you just care about building U-Boot though.
class Pcduino3UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "

    build = Pcduino3UBootBuilder()

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class Pcduino3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    # Username for logging in once linux has booted
    username = "pi"
    # Password.  If you don't need a password, set this to `None`
    password = "raspberry"

# tbot will check for `BOARD`, don't forget to set it!
BOARD = Pcduino3
UBOOT = Pcduino3UBoot
# You need to set `LINUX` now as well.
LINUX = Pcduino3Linux
