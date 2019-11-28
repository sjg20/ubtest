#! bin/bash

# Script to set up this user to be able to execute jobs from gitlab
ROOT=/home/gitlabber
BUILDMAN=${ROOT}/u-boot/tools/buildman/buildman
OUT=${ROOT}/out

clone() {
    echo clone
    git clone --depth 1 https://gitlab.denx.de/u-boot/custodians/u-boot-dm.git u-boot
}

toolchains() {
    echo toolchains
    ${BUILDMAN} --fetch-arch arm,aarch64,i386
}

build_tools() {
    echo build tools
    sudo apt-get install -y build-essential swig iasl device-tree-compiler \
        bison flex libisl-dev gcc-arm-none-eabi python3-pytest
}

test_build() {
    cd u-boot
    mkdir -p ${OUT}
    ${BUILDMAN} -o ${OUT} --board rpi_3
}

test_hooks() {
    cd "${ROOT}"
    git clone https://gitlab.denx.de/u-boot/u-boot-test-hooks.git
}

# Main program

[[ ! -e u-boot ]] && clone
[[ ! -e ~/.buildman-toolchains ]] && toolchains
which dtc >/dev/null || build_tools
[[ ! -e "${ROOT}/u-boot-test-hooks" ]] && test_hooks

# Need to provide:
# /usr/lib/x86_64-linux-gnu/libisl.so.15*
# /usr/lib/x86_64-linux-gnu/libmpfr.so.4*

# test_build()
