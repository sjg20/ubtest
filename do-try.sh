#!/bin/bash

board=$1
rev=$(git rev-parse $2)
commit=$3

if [[ -z "$board" ]] || [[ -z "$rev" ]]; then
	echo "Usage: $0 <board> <commit>"
	echo
	echo "<commit> is a branch/commit on ellesmere/u-boot.git"
	exit 1
fi

echo "Revision ${rev}, board ${board}"
cd /vid/software/devel/ubtest
echo
echo "Checking revision ${rev}"
tbot -l kea.py -b ${board}.py -p rev=\"${rev}\" -p clean=True \
    uboot_checkout && \
tbot -l kea.py -b ${board}.py -p clean=False -T tbot/contrib \
    uboot_build_and_flash && \
sleep 2 && \
tbot -vv -l kea.py -b ${board}.py uboot_smoke_test
