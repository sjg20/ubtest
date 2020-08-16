#!/bin/bash

. get_args.sh

tbot -l kea.py -b ${board}.py -p rev=\"${rev}\" -p clean=${clean} \
    uboot_checkout && \
tbot -l kea.py -b ${board}.py -T tbot/contrib -p clean=${clean} \
    uboot_build_send_interactive
