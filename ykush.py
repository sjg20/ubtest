import time

class Ykush(object):
    def ykush_on(self, host, serial, port):
        host.exec0("ykushcmd", "-s", serial, "-u", port)

    def ykush_off(self, host, serial, port):
        host.exec0("ykushcmd", "-s", serial, "-d", port)

    def ykush_is_on(self, host, serial, port):
        out = host.exec0("ykushcmd", "-s", serial, "-g", port)
        return 'ON' in out

    def ykush_reset(self, host, serial, port):
        if self.ykush_is_on(host, serial, port):
            self.ykush_off(host, serial, port)
            time.sleep(1)
        self.ykush_on(host, serial, port)
