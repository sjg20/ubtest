#!/bin/sh

set -ex

#V=-v

# Run coreboot under QEMU

CBDIR=/scratch/sglass/coreboot/build
BUILD_DIR=/tmp/b/coreboot
#ISO=/vid/software/linux/debian/debian-11.5.0-i386-DVD-1.iso
ISO=/vid/software/linux/debian/debian-32.img
#
#cp $UBTEST/coreboot.rom.in $BUILD_DIR/coreboot.rom
cp $CBDIR/coreboot.rom $BUILD_DIR/coreboot.rom

cbfstool $BUILD_DIR/coreboot.rom remove -n fallback/payload || true

cbfstool $BUILD_DIR/coreboot.rom add-flat-binary -f $BUILD_DIR/u-boot.bin \
	-n fallback/payload -c LZMA -l 0x1110000 -e 0x1110000;

qemu-system-x86_64 -bios $BUILD_DIR/coreboot.rom -serial mon:stdio \
 	-smp cpus=2 -m 1G
exit 0

qemu-system-x86_64 -bios $BUILD_DIR/coreboot.rom -serial mon:stdio \
 	-smp cpus=2 -m 1G \
 	-drive id=disk,file=$ISO,if=none \
 	-device ahci,id=ahci \
 	-device ide-hd,drive=disk,bus=ahci.0

#	-cdrom $ISO -nographic

# qemu-system-x86_64 -m 4G -bios $BUILD_DIR/coreboot.rom -serial mon:stdio \
# 	-drive id=disk,file=$ISO,if=none \
# 	-device ahci,id=ahci \
# 	-device ide-hd,drive=disk,bus=ahci.0

#	-drive id=disk,file=$ISO,if=none \
#	-device ich9-ahci,id=ahci \
#	-device ide-hd,drive=disk,bus=ahci.0

