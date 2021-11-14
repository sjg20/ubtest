#!/bin/sh

set -ex

#V=-v

# Run a test on ARM with qemu

test=$1

crosfw qemu_arm_spl
PATH=$PATH:/vid/software/devel/ubtest/u-boot-test-hooks/ test/py/test.py \
	-B qemu_arm_spl --id na --build-dir /tmp/b/qemu_arm_spl -k ${test}
