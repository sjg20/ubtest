#!/bin/sh

set -ex

#V=-v

# Run a test on ARM with qemu

test=$1

crosfw qemu-ppce500
PATH=$PATH:/vid/software/devel/ubtest/u-boot-test-hooks/ test/py/test.py \
	-B qemu-ppce500 --id na --build-dir /tmp/b/qemu-ppce500 -k ${test}
