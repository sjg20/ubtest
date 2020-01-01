class Sdwire(object):
    def sdwire_dut(self):
        self.host.exec0("sd-mux-ctrl", "--device-serial",
                        self.sdwire_serial, '--dut')

    def sdwire_ts(self):
        self.host.exec0("sd-mux-ctrl", "--device-serial",
                        self.sdwire_serial, '--ts')
