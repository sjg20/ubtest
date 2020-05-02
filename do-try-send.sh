#!/bin/bash

clean=False
if [ "$1" == "-f" ]; then
    clean=True
    shift
fi

board=$1
rev=$(git rev-parse $2)

echo "Revision ${rev}, board ${board}"
cd /vid/software/devel/ubtest
echo
echo "Checking revision ${rev}"
tbot -l kea.py -b ${board}.py -p rev=\"${rev}\" -p clean=${clean} \
    uboot_checkout && \
tbot -l kea.py -b ${board}.py -T tbot/contrib -p clean=${clean} \
    uboot_build_send_interactive
