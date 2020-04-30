import time
import dlipower

class Dli(object):
    """Intended to be included as a subclass of the board that needs it

    Properties provided by base class:
        host: Lab host
        dli_hostname: IP address or host name of power (e.g "192.168.0.100")
        dli_user: User name to use (e.g. "admim")
        dli_password: Password to use (e.g. "1234")
        dli_outlet: Outlet to control (1-8)
    """
    switch = None

    def dli_setup(self):
        if not self.switch:
            self.switch = dlipower.PowerSwitch(hostname=self.dli_hostname,
                userid=self.dli_user, password=self.dli_password)

    def dli_on(self):
        self.dli_setup()
        self.switch.on(self.dli_outlet)

    def dli_off(self):
        self.dli_setup()
        self.switch.off(self.dli_outlet)

    def dli_reset(self):
        self.dli_off()
        time.sleep(1)
        self.dli_on()
