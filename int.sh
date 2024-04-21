#!/bin/bash

set -e

usage() {
	echo Error: $1

	echo "Open an interactive console to a board"
	echo
	echo "Usage: $0 [-V] <board>"
	exit 1
}

while getopts "v" opt; do
	case $opt in
	v )
#	  V=-vv
	  V=-v
	  ;;
	\? )
	  echo "Invalid option: $OPTARG" 1>&2
	  ;;
	esac
done

shift $((OPTIND -1))

board=$1
[[ -z "$board" ]] && usage "No board $board"

# cd /vid/software/devel/ubtest
# tbot $V -l kea.py -b ${board}.py interactive_board

LG_CROSSBAR=ws://kea:20408/ws labgrid-client \
	${V} -c /vid/software/devel/ubtest/lab/env_rpi_try.cfg \
	-p ${board} -s start console
