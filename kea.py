import tbot
from tbot.machine import connector, linux

class KeaLab(
    connector.ParamikoConnector,
    linux.Bash,
    linux.Lab,
):
    name = "sglass"
    hostname = "kea"

    @property
    def workdir(self):
        return linux.Workdir.athome(self, "tbot-workdir")


# tbot will check for `LAB`, don't forget to set it!
LAB = KeaLab
