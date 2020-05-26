#!/bin/bash

board=$1

if [[ -z "$board" ]]; then
	echo "Usage: $0 <board>"
	echo
	echo "Does 'git bisect run' on a board"
	exit 1
fi

git bisect run /vid/software/devel/ubtest/do-try.sh ${board} HEAD
