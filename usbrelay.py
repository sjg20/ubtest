import time

class Usbrelay(object):
    """Intended to be included as a subclass of the board that needs it

    Properties provided by base class:
        host: Lab host
        usbrelay_power: Relay number of power button
        usbrelay_reset: Relay number of reset button
        usbrelay_recovery: Relay number of recovery button
    """
    def usbrelay_set_power(self, value):
        self.usbrelay_set(self.usbrelay_power, value)

    def usbrelay_set_reset(self, value):
        self.usbrelay_set(self.usbrelay_reset, value)

    def usbrelay_set_recovery(self, value):
        self.usbrelay_set(self.usbrelay_recovery, value)

    def usbrelay_set(self, relay, value):
        self.host.exec0("usbrelay", "%s%d=%d" %
                        (self.usbrelay_name, relay, value))
