#!/bin/sh

cd etc
cp /etc/udev/rules.d/*.rules udev/.
cp /etc/fstab .
cp /etc/ssh/sshd_config .
cp /etc/hosts .
cp /etc/systemd/system/systemd-udevd.service.d/override.conf .
cp /etc/group .
