#!/bin/bash

set -e

lab=kea.py
V=
clean=False

usage() {
	echo Error: $1

	echo "Usage: [-cv] $0 <board> [<commit>]"
	echo
	echo "   -c  - clean before building"
	echo "   -v  - use verbose output"
	echo
	echo "<commit> is a branch/commit on the tree used by tbot"
	echo "If <commit> is empty, the current source is used"
	exit 1
}

while getopts "cv" opt; do
	case $opt in
	c )
	  clean=True
	  ;;
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
	git diff --no-ext-diff HEAD >$patch
	[[ ! -s $patch ]] && patch=
	patch="${patch:+"-p patch=\"$patch\""}"
	if [[ -n "$patch" ]]; then
		echo "Sending patch file with uncommitted changes"
	fi
fi

rev=$(git rev-parse $commit)

if [[ -z "$rev" ]]; then
	usage "No revision $rev"
fi

echo "Revision ${rev}, board ${board}"
cd /vid/software/devel/ubtest
echo
echo "Checking revision ${rev}"
pwd
