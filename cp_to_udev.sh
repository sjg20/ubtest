#!/bin/sh

cd etc
cp udev/* /etc/udev/rules.d/
cp fstab /etc/.
udevadm control -R
