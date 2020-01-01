import tbot
from tbot.machine import board, channel, connector, linux
from servo import Servo

class Chromebook(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Servo,
):
    def poweron(self) -> None:
        """Procedure to turn power on."""

        # You can access the labhost as `self.host` (if you use the
        # ConsoleConnector).  In this case I have a simple command to
        # toggle power.
        self.servo_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.servo_off()

    def connect(self, mach) -> channel.Channel:
        """Connect to the boards serial interface."""

        # `mach.open_channel` 'steals' mach's channel and runs the
        # given command to connect to the serial console.  Your command
        # should just connect its tty to the serial console like rlogin,
        # telnet, picocom or kermit do.  The minicom behavior will not work.
        tty = self.servo_get_tty()
        return mach.open_channel("picocom", "-b", "115200", tty)


# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class ChromebookLinux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    pass
