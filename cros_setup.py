#!/usr/bin/python3

"""
This utility starts up servo daemons for all boards mentioned in the servodrc
file
"""

import os
import select
import shutil
import subprocess
import sys
import time
from cros_constants import DUT_CONTROL, SERVOD, RCFILE, LOGDIR

STATE_INIT, STATE_WAIT, STATE_ERROR, STATE_READY = range(4)

class Servo(object):
    """Handle a servo board

    This supports starting a servod daemon for the board and checking the
    progress of the daemon.

    Properties:
        name: Name of board, as per the rc file (e.g. 'samus')
        port: Port number for the servo daemon (e.g. 9900)
        proc: Subprocess for the servo daemon, or None if not started
        fd: File descriptor for the daemon's 'info' file, None if not started
        ready: True if the servo daemon is ready to serve traffic
        logs: Directory used by the daemon for log files
        info_file: Filename of the daemon's 'info' file
        state: Current STATE_... of this servo
        buf: Buffer containing date read from @info_file. We read out from this
            a line at a time
        errs: List of error messages written by servod into the @info_file
    """
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.proc = None
        self.fd = None
        self.ready = False
        self.logs = os.path.join(LOGDIR, 'servod_%s' % self.port)
        self.info_file = os.path.join(self.logs, 'latest.INFO')
        self.state = STATE_INIT
        self.buf = b''
        self.errs = []

    def remove_logs(self):
        """Remove any pre-existing logs for this daemon"""
        os.system('sudo rm -rf "%s"' % self.logs)

    def start(self):
        """Start the servo daemon and wait until its log file can be accessed"""
        if not os.path.exists(self.logs):
            os.mkdir(self.logs)

        cmd = ['sudo', SERVOD, '--rcfile', RCFILE, '--name', self.name,
               '--port', self.port, '--log-dir', LOGDIR]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        while not os.path.exists(self.info_file):
            time.sleep(.1)
        self.fd = os.open(self.info_file, os.O_RDONLY)
        if not self.fd:
            raise ValueError("Cannot open file '%s'" % self.info_file)
        self.state = STATE_WAIT

    def process_data(self, data):
        """Process data received from servod, waiting for it to be ready

        Returns:
            True if servo is ready, False if not
        """
        self.buf += data
        while b'\n' in self.buf:
            pos = self.buf.find(b'\n')
            line = self.buf[:pos]
            self.buf = self.buf[pos + 1:]
            #print('line', line)
            if b'Listening on localhost' in line:
                print('%s is ready' % self.name)
                self.state = STATE_READY
                return True
            elif b'ERROR' in line:
                pos = line.rfind(b' - ')
                err = line[pos + 3:]
                if err not in self.errs:
                    print('%s got error: %s' % (self.name, err))
                    self.errs.append(err)
        return False

    def active(self):
        if self.state in (STATE_INIT, STATE_ERROR):
            return False
        elif self.state == STATE_WAIT:
            if self.proc.poll() is None:
                return True
        elif self.state == STATE_READY:
            return True

    def kill(self):
        self.proc.kill()

class Servos(object):
    """Handle a group of servo boards

    This handles multiple Servo objects, allowing them to be started up, etc.

    Properties:
        rcfile: Filename of the servodrc file
        servos: List of servos we know about
    """
    def __init__(self):
        self.rcfile = RCFILE
        self.servos = []

    def read(self):
        """read the servodrc file to get information about attach boards"""
        servos = []
        with open(self.rcfile) as fd:
            for line in fd.readlines():
                if line.startswith('#'):
                    continue
                vals = [item.strip() for item in line.split(',')]
                if len(vals) == 4:
                    name, serial, port, board = vals
                    servo = Servo(name, port)
                    self.servos.append(servo)

    def remove_logs(self):
        """Remove logs for all known servo daemons"""
        for servo in self.servos:
            servo.remove_logs()

    def start(self):
        """Start a servo daemon for each board"""
        for servo in self.servos:
            servo.start()

    def wait_ready(self):
        """Monitor the servod log files until all boards are ready"""
        todo = {servo.fd: servo for servo in self.servos}
        fds = [servo.fd for servo in todo.values()]
        err_count = 0
        while todo:
            readfds, _, _ = select.select(fds, [], [], 2.0)
            for readfd in readfds:
                servo = todo.get(readfd)
                if servo:
                    data = os.read(readfd, 1000)
                    if data:
                        if servo.process_data(data):
                            del todo[readfd]
                    else:
                        break
            for servo in todo.values():
                if not servo.active():
                    #print 'not active'
                    del todo[servo.fd]
                    err_count += 1
                    data = os.read(servo.fd, 1000)
                    servo.process_data(data)
        print('%d ready, %d error' % (len(self.servos) - err_count, err_count))

    def get_port_by_name(self, name):
        """Get the servod port number for a board

        Args:
            name: Name of board to check

        Returns:
            port number, as a string
        """
        for servo in self.servos:
            if servo.name == name:
                return servo.port
        raise ValueError("No such servo '%s'" % name)

    def kill(self):
        for servo in self.servos:
            try:
                servo.kill()
            except:
                pass

    def setup_pts(self):
        for servo in self.servos:
            if servo.state == STATE_READY:
                cmd = [DUT_CONTROL, '-p', servo.port, 'cpu_uart_pty']
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate(timeout=5)
                pts = stdout.strip().split(b':')[-1]
                cmd = ['sudo', 'chmod', 'a+rw', pts]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                proc.communicate(timeout=1)


if __name__ == "__main__":
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
    servos = Servos()
    servos.read()
    servos.remove_logs()
    try:
        servos.start()
        servos.wait_ready()
        servos.setup_pts()

        print('ready - press Ctrl-C to stop')
        while True:
            time.sleep(1)
    finally:
        servos.kill()
