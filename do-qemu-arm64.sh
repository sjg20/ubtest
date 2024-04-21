#!/bin/sh

#set -ex

#V=-v

# Run a test on ARM with qemu

. "$(dirname $0)/hooks.sh"

# set_build qemu_arm64

build_and_run qemu_arm64 $1
# crosfw qemu_arm64
# test/py/test.py \
# 	-B qemu_arm64 --id na --build-dir /tmp/b/qemu_arm64 -k ${test}
