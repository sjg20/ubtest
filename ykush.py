class Ykush(object):
    def ykush_on(self, host, serial, port):
        host.exec0("ykushcmd", "-s", serial, "-u", port)

    def ykush_off(self, host, serial, port):
        host.exec0("ykushcmd", "-s", serial, "-d", port)
