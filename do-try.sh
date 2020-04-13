#!/bin/sh

board=$1
rev=$(git rev-parse $2)

cd /vid/software/devel/ubtest
echo
echo "Checking revision ${rev}"
tbot -l kea.py -b ${board}.py -p rev=\"${rev}\" -p clean=True \
    uboot_checkout && \
tbot -l kea.py -b ${board}.py -p clean=False -T tbot/contrib -v \
    uboot_build_and_flash && \
sleep 2 && \
tbot -l kea.py -b ${board}.py uboot_boots
