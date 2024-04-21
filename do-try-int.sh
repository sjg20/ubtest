#!/bin/bash

mydir=$(dirname $(readlink $0))

. ${mydir}/get_args.sh

# tbot -l ${lab} -b ${board}.py -T tbot/contrib -p rev=\"${rev}\" \
# 	-p clean=${clean} $patch $V uboot_build_and_flash
# tbot -l ${lab} -b ${board}.py interactive_board

LG_CROSSBAR=ws://kea:20408/ws labgrid-client \
	${V} -c /vid/software/devel/ubtest/lab/env_rpi_try.cfg \
	-V do-bootstrap 1 -V do-build 1 \
	-p ${board} -s start console
