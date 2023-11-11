#!/bin/sh

set -ex

#V=-v

# Run a test on x86 64-bit with qemu

test=$1

CBDIR=/scratch/sglass/coreboot/build

UBTEST=/vid/software/devel/ubtest/
BUILD_DIR=/tmp/b/coreboot

#cp $UBTEST/coreboot.rom.in $BUILD_DIR/coreboot.rom
cp $CBDIR/coreboot.rom $BUILD_DIR/coreboot.rom

cbfstool $BUILD_DIR/coreboot.rom remove -n fallback/payload || true

cbfstool $BUILD_DIR/coreboot.rom add-flat-binary -f $BUILD_DIR/u-boot.bin \
	-n fallback/payload -c LZMA -l 0x1110000 -e 0x1110000;

PATH=$PATH:$UBTEST/u-boot-test-hooks/ test/py/test.py \
	-B coreboot --id qemu --build-dir $BUILD_DIR -k ${test}
