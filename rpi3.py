import tbot
from tbot.machine import board, channel, connector, linux
from ykush import Ykush
from sdwire import Sdwire

class Rpi3(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Ykush,
    Sdwire,
):
    name = "Raspberry Pi 3b"
    ykush_serial = "YK17698"
    ykush_port = "1"

    sdwire_serial = "sdwire-18"

    def poweron(self) -> None:
        """Procedure to turn power on."""

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.sdwire_dut(self.host, self.sdwire_serial)
        self.ykush_on(self.host, self.ykush_serial, self.ykush_port)

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.ykush_off(self.host, self.ykush_serial, self.ykush_port)
        self.sdwire_ts(self.host, self.sdwire_serial)

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        return mach.open_channel("picocom", "-b", "115200", "/dev/ttyusb_port1")

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class Rpi3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    # Username for logging in once linux has booted
    username = "pi"
    # Password.  If you don't need a password, set this to `None`
    password = "raspberry"

# tbot will check for `BOARD`, don't forget to set it!
BOARD = Rpi3
# You need to set `LINUX` now as well.
LINUX = Rpi3Linux
