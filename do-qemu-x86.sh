#!/bin/sh

set -ex

#V=-v

# Run a test on x86 32-bit with qemu

test=$1

crosfw qemu-x86
PATH=$PATH:/vid/software/devel/ubtest/u-boot-test-hooks/ test/py/test.py \
	-B qemu-x86 --id na --build-dir /tmp/b/qemu-x86 -k ${test}
