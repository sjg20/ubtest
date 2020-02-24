import time
import tbot
from tbot.machine import board, channel, connector, linux
from dli import Dli
from usbrelay import Usbrelay
from sdwire import Sdwire

class PumaPc(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Usbrelay,
    Dli,
    Sdwire,
):
    name = "puma"
    usbrelay_name = "6QMBS_"
    usbrelay_power = 8
    usbrelay_reset = 7

    dli_hostname = "192.168.4.19"
    dli_user = "admin"
    dli_password = "1234"
    dli_outlet = 2

    sdwire_serial = "202001064005"

    #ether_mac = "02:4f:04:03:26:d1"

    def poweron(self) -> None:
        """Procedure to turn power on."""

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.dli_off()
        time.sleep(.5)
        self.dli_on()

        self.usbrelay_set_power(True)
        time.sleep(1)
        self.usbrelay_set_power(False)

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        pass

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port6")

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class PumaPcLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    # Username for logging in once linux has booted
    username = ""
    # Password.  If you don't need a password, set this to `None`
    password = ""

# tbot will check for `BOARD`, don't forget to set it!
BOARD = PumaPc
# You need to set `LINUX` now as well.
LINUX = PumaPcLinux
