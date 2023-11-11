#!/bin/sh

set -ex

#V=-v

# Run a test on x86 64-bit with qemu

test=$1

UBTEST=/vid/software/devel/ubtest/
BUILD_DIR=/tmp/b/coreboot64

cp $UBTEST/coreboot.rom.in $BUILD_DIR/coreboot.rom
cbfstool $BUILD_DIR/coreboot.rom add-flat-binary -f $BUILD_DIR/spl/u-boot-spl.bin \
	-n fallback/payload -c LZMA -l 0x1110000 -e 0x1110000;

PATH=$PATH:$UBTEST/u-boot-test-hooks/ test/py/test.py \
	-B coreboot64 --id qemu --build-dir $BUILD_DIR -k ${test}
