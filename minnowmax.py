import tbot
from tbot.machine import board, channel, connector, linux
from dli import Dli

class Minnowmax(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Dli,
):
    dli_hostname = "192.168.4.19"
    dli_user = "admin"
    dli_password = "1234"
    dli_outlet = 6

    def poweron(self) -> None:
        """Procedure to turn power on."""

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.dli_on()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port7")


# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class MinnowmaxLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    pass

# tbot will check for `BOARD`, don't forget to set it!
BOARD = Minnowmax
# You need to set `LINUX` now as well.
LINUX = MinnowmaxLinux
