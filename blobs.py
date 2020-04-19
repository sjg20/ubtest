import os
import time

from tbot.tc import git, shell

class Blobs:
    def add_blobs(self, repo: git.GitRepository) -> None:
        bindir = os.path.join(repo._local_str(), self.blob_dest)
        repo.host.exec0("bash", "-c", "cp %s %s" % (self.blob_src, bindir))
