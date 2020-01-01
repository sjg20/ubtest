class Sdwire(object):
    """Intended to be included as a subclass of the board that needs it

    Properties provided by base class:
        host: Lab host
        sdwire_serial: Serial number of SDwire device
    """
    def sdwire_dut(self):
        self.host.exec0("sd-mux-ctrl", "--device-serial",
                        self.sdwire_serial, '--dut')

    def sdwire_ts(self):
        self.host.exec0("sd-mux-ctrl", "--device-serial",
                        self.sdwire_serial, '--ts')
