#!/bin/sh

set -ex

#V=-v

# Run a test on x86 64-bit with qemu

test=$1

crosfw qemu-x86_64
PATH=$PATH:/vid/software/devel/ubtest/u-boot-test-hooks/ test/py/test.py \
	-B qemu-x86_64 --id na --build-dir /tmp/b/qemu-x86_64 -k ${test}
