#!/bin/sh

set -ex

#V=-v

# Run a test on ARM with qemu

test=$1

crosfw qemu_arm64
PATH=$PATH:/vid/software/devel/ubtest/u-boot-test-hooks/ test/py/test.py \
	-B qemu_arm64 --id na --build-dir /tmp/b/qemu_arm64 -k ${test}
