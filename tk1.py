import time
import tbot
from tbot.machine import board, channel, connector, linux
from usbrelay import Usbrelay

class Tk1(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Usbrelay
):
    name = "tk1"

    usbrelay_power=1
    usbrelay_reset=2
    usbrelay_recovery=3

    #ether_mac = "02:4f:04:03:26:d1"

    def poweron(self) -> None:
        """Procedure to turn power on."""

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.usbrelay_set_reset(True)
        time.sleep(.25)
        self.usbrelay_set_reset(False)

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        pass

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port3")

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class Tk1Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    # Username for logging in once linux has booted
    username = ""
    # Password.  If you don't need a password, set this to `None`
    password = ""

# tbot will check for `BOARD`, don't forget to set it!
BOARD = Tk1
# You need to set `LINUX` now as well.
LINUX = Tk1Linux
