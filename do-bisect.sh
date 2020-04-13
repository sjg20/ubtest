#!/bin/sh

board=$1
git bisect run /vid/software/devel/ubtest/do-try.sh ${board} HEAD
