import os
import sys

import cros_setup
from cros_constants import DUT_CONTROL, UBTEST
import tbot

sys.path.append(os.path.join(UBTEST, "u-boot", "tools", "patman"))
import command

class Servo:
    """Intended to be included as a subclass of the board that needs it

    Properties provided by base class:
        host: Lab host
        ykush_serial: Serial number of YKUSH device
        ykush_port: Port number on that device
    """
    #servo_port = None

    #def servo_setup(self):
        #if not self.servo_port:
            #servos = cros_setup.Servos()
            #servos.read()
            #self.servo_port = servos.get_port_by_name(self.name)

    def servo_on(self):
        self.servo_reset()

    def servo_off(self):
        self.dut_control("pwr_button:press", "sleep:2", "pwr_button:release")

    def servo_reset(self):
        self.dut_control("cold_reset:on", "sleep:.2", "cold_reset:off")

    def dut_control(self, *args):
        #self.servo_setup()
        return self.host.exec0(DUT_CONTROL, "-p", str(self.servo_port), *args)

    def servo_get_tty(self):
        pty = self.dut_control("cpu_uart_pty").strip().split(':')[1]
        tbot.log.message("%s is on port %s and uses %s" %
                         (self.name, self.servo_port, pty))
        return pty
