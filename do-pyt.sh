#!/bin/bash

# work in progress













mydir=$(dirname $(readlink $0))

# Run a pytest on sandbox
# $1: Name of test to run (optional, else run all)

function pyt {
	local tests="$1"

	shift
	test/py/test.py -B sandbox --build-dir /tmp/b/sandbox ${tests:+"-k $tests"} $@
}

# Run a pytest on a baord
# $b is the board
# $1: Name of test to run  (optional, else run all SPL tests)
function pyt_any {
	local run

	if [ "$1" = "-b" ]; then
		crosfw $b || return 1
		shift
	fi

	[[ -z "$run" ]] && run='test_ofplatdata or test_handoff or test_spl'
	test/py/test.py -B $b --build-dir /tmp/b/$b -k "$run"
}
