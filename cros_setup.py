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
from cros_constants import SERVOD, RCFILE, LOGDIR

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
    """
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.proc = None
        self.fd = None
        self.ready = False
        self.logs = os.path.join(LOGDIR, 'servod_%s' % self.port)
        self.info_file = os.path.join(self.logs, 'latest.INFO')

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

    def process_data(self, data):
        """Process data received from servod, waiting for it to be ready"""
        for line in data.splitlines():
            #print('line', line)
            if b'Listening on localhost' in line:
                self.ready = True
                print('%s is ready' % self.name)
        return self.ready


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
        while todo:
            readfds, _, _ = select.select(fds, [], [], 2.0)
            for readfd in readfds:
                servo = todo.get(readfd)
                if servo:
                    data = os.read(readfd, 100)
                    if data:
                        if servo.process_data(data):
                            del todo[readfd]
                    else:
                        break
        print('All ready')

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


if __name__ == "__main__":
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
    servos = Servos()
    servos.read()
    servos.remove_logs()
    servos.start()
    servos.wait_ready()

    print('ready - press Ctrl-C to stop')
    while True:
        time.sleep(1)
