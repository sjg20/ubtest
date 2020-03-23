import time

class Ykush(object):
    """Intended to be included as a subclass of the board that needs it

    Properties provided by base class:
        host: Lab host
        ykush_serial: Serial number of YKUSH device
        ykush_port: Port number on that device
    """
    def ykush_on(self):
        print("ykush_on")
        self.host.exec0('ykushcmd', '-s', self.ykush_serial,
                        '-u', self.ykush_port)

    def ykush_off(self):
        self.host.exec0('ykushcmd', '-s', self.ykush_serial,
                        '-d', self.ykush_port)

    def ykush_is_on(self):
        out = self.host.exec0('ykushcmd', '-s', self.ykush_serial,
                              '-g', self.ykush_port)
        return 'ON' in out

    def ykush_reset(self):
        if self.ykush_is_on():
            self.ykush_off()
            time.sleep(1)
        self.ykush_on()
