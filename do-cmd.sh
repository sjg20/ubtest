#!/bin/bash

set -ex

crosfw sandbox
/tmp/b/sandbox/u-boot -c "mw.q 0 123456789abc; md.q 0 1" |grep 123456789abc
