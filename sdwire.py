class Sdwire(object):
    def sdwire_dut(self, host, serial):
        host.exec0("sd-mux-ctrl", "--device-serial", serial, '--dut')

    def sdwire_ts(self, host, serial):
        host.exec0("sd-mux-ctrl", "--device-serial", serial, '--ts')
