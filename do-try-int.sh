#!/bin/bash

set -e

#V=-vv
usage() {
	echo Error: $1

	echo "Usage: $0 <board> [<commit>]"
	echo
	echo "<commit> is a branch/commit on ellesmere/u-boot.git"
	echo "If <commit> is empty, the current source is used"
	exit 1
}

while getopts "v" opt; do
	case $opt in
	v )
	  V=-vv
	  ;;
	\? )
	  echo "Invalid option: $OPTARG" 1>&2
	  ;;
	esac
done

shift $((OPTIND -1))

board=$1
[[ -z "$board" ]] && usage "No board $board"

commit=$2

if [[ -z "$commit" ]]; then
	commit=HEAD
	patch=/tmp/$$.patch
	git diff --no-ext-diff >$patch
	[[ ! -s $patch ]] && patch=
	patch="${patch:+"-p patch=\"$patch\""}"
	echo "Sending patch file with uncommitted changes"
fi

rev=$(git rev-parse $commit)

if [[ -z "$rev" ]]; then
	usage "No revision $rev"
fi

cd /vid/software/devel/ubtest
echo
echo "Checking revision ${rev}"
# tbot -l kea.py -b ${board}.py -p rev=\"${rev}\" -p clean=True $patch $V \
#     uboot_checkout
tbot -l kea.py -b ${board}.py -T tbot/contrib -p rev=\"${rev}\" \
	-p clean=False $patch $V uboot_build_and_flash
tbot -l kea.py -b ${board}.py interactive_board
