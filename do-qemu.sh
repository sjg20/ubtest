#!/bin/sh

set -ex

#V=-v

# Run a test on ARM with qemu

test=$1

crosfw qemu_arm
PATH=$PATH:/vid/software/devel/ubtest/u-boot-test-hooks/ test/py/test.py \
	-B qemu_arm --id na --build-dir /tmp/b/qemu_arm -k ${test}
