import tbot
from tbot.machine import board, channel, connector, linux
from chromebook import Chromebook, ChromebookLinux

class NyanBig(
    Chromebook
):
    name = "Nyan Big"
    servo_name = "nyan-big"

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class NyanBigLinux(
    ChromebookLinux
):
    # Username for logging in once linux has booted
    username = "root"
    # Password.  If you don't need a password, set this to `None`
    password = "test0000"


# tbot will check for `BOARD`, don't forget to set it!
BOARD = NyanBig
# You need to set `LINUX` now as well.
LINUX = NyanBigLinux
