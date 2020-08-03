#!/usr/bin/python3

import os
import sys

boards = {
    'pcduino3' : 'Linksprite_pcDuino3',
    'rpi_3b': 'rpi_3_32b',
    'opi_pc': 'orangepi_pc',
    'tk1': 'jetson-tk1',
    'zynq_zybo': 'zynq_zybo',
    }

def doit(board):
    config = boards[board]
    cmd = ['test/py/test.py', '-B', config, '--id', 'sjg-%s' % board,
           '--build-dir', '../current/%s' % config, '-k', 'test_help']
    os.system(' '.join(cmd))


doit(board=sys.argv[1])
