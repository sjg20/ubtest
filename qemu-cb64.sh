#!/bin/sh

set -ex

#V=-v

# Run coreboot64 under QEMU

UBTEST=/vid/software/devel/ubtest/
BUILD_DIR=/tmp/b/coreboot64
#BUILD_DIR=/scratch/sglass/coreboot/tmp/b/coreboot64
DISK=/vid/software/linux/ubuntu/ubuntu-23.04-desktop-amd64.iso
# DISK=/vid/software/linux/debian/debian-32.img
# DISK=/vid/software/win/virtio-win-0.1.229.iso
DISK=/vid/software/win/Win10_21H2_English_x64.iso
# DISK=/vid/software/win/Win11_22H2_English_x64v2.iso

cp /scratch/sglass/coreboot/build/coreboot.rom $BUILD_DIR/coreboot.rom
#cp $UBTEST/coreboot.rom.in $BUILD_DIR/coreboot.rom

# update u-boot
cbfstool $BUILD_DIR/coreboot.rom remove -n fallback/payload || true
cbfstool $BUILD_DIR/coreboot.rom add-flat-binary \
	-f $BUILD_DIR/u-boot-x86-with-spl.bin \
	-n fallback/payload -c LZMA -l 0x1110000 -e 0x1110000

#-M accel=kvm

qemu-system-x86_64 -M accel=kvm -m 4G -smp 4 -bios $BUILD_DIR/coreboot.rom \
	-serial mon:stdio \
	-monitor telnet:127.0.0.1:55555,server,nowait \
	\
	-drive id=root,file=root.img,if=none,format=qcow2 \
	-device ich9-ahci,id=ahcir \
	-device ide-hd,drive=root,bus=ahcir.0 \
	\
	-drive id=disk,file=$DISK,if=none \
	-device ich9-ahci,id=ahci \
	-device ide-hd,drive=disk,bus=ahci.0
