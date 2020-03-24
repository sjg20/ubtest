import tbot
from tbot.machine import board, channel, connector, linux
from chromebook import Chromebook, ChromebookLinux

class Link(
    Chromebook
):
    name = "Link"
    servo_name = "link"
    ether_mac = "94:eb:2c:00:03:b6"

# Linux machine
#
# We use a config which boots directly to Linux without interaction
# with a bootloader for this example.
class LinkLinux(
    ChromebookLinux
):
    # Username for logging in once linux has booted
    username = "root"
    # Password.  If you don't need a password, set this to `None`
    password = "test0000"

# Not sure if this the correct config for this boards U-Boot ... It does not
# matter if you just care about building U-Boot though.
class LinkUBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "

    build = LinkBootBuilder()


# tbot will check for `BOARD`, don't forget to set it!
BOARD = Link
UBOOT = LinkUBoot
# You need to set `LINUX` now as well.
LINUX = LinkLinux
