#!/bin/bash

mydir=$(dirname $(readlink $0))

. ${mydir}/get_args.sh

tbot -l ${lab} -b ${board}.py -T tbot/contrib -p rev=\"${rev}\" \
	-p clean=${clean} $patch $V uboot_build_and_flash
tbot -l ${lab} -b ${board}.py interactive_board
