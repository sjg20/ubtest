#!/usr/bin/python3

import re
import subprocess

def find_bus_dev(vendor, product=None):
    match = '%04x' % vendor
    if product:
        match += ':%04x' % product
    cmd = ['lsusb', '-d', match]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=1)
    bus_dev_list = []
    for line in stdout.splitlines():
        # Bus 004 Device 016: ID 04d8:f2f7 Microchip Technology, Inc.
        m = re.match(b'Bus (\d{3}) Device (\d{3})', line)
        if not m:
            raise ValueError('No such device %04x:%04x' % (vendor, product))
        bus_dev_list.append([int(m.group(1)), int(m.group(2))])
    return bus_dev_list

def find_path(bus, dev):
    cmd = ['udevadm', 'info', '--name=/dev/bus/usb/%03d/%03d' % (bus, dev)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=1)
    line = stdout.splitlines()[0]
    # P: /devices/pci0000:00/0000:00:14.0/usb4/4-10/4-10.1/4-10.1.3/4-10.1.3.4
    addr = line.split(b'/')[-1]
    return addr

def trigger(addr):
    cmd = ['sudo', 'udevadm', 'test',
           '/sys/bus/usb/devices/%s' % addr.decode('utf-8')]
    print(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=1)

dev_types = {
   'sdwire': [0x04e8, 0x6001],
   'ttyusb': [0x067b, 0x2303],
   'ykusb': [0x04d8, 0xf2f7],
   'tegra': [0x0955, 0x7140],
   'relay': [0x16c0, 0x05df],
   'em100': [0x04b4, 0x1235],
}

for dev_type, (vendor, product) in dev_types.items():
    bus_dev_list = find_bus_dev(vendor, product)
    for bus, dev in bus_dev_list:
        print('udevadm info --name=/dev/bus/usb/%03d/%03d --attribute-walk' %
              (bus, dev))
        addr = find_path(bus, dev)
        trigger(addr)
