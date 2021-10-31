#!/usr/bin/python3

import os
import sys

builds = {
    'pcduino3' : 'Linksprite_pcDuino3',
    'rpi3': 'rpi_3_32b',
    'opi_pc': 'orangepi_pc',
    'tk1': 'jetson-tk1',
    'zynq_zybo': 'zynq_zybo',
    }

official_boards = {
    'rpi3': 'rpi_3b',
}

def doit(board):
    config = builds[board]
    official_board = official_boards.get(board, board)

    cmd = ['test/py/test.py', '-B', config, '--id', 'sjg-%s' % official_board,
           '--build-dir', '../current/%s' % config, '-k', 'test_help']
    os.system(' '.join(cmd))


doit(board=sys.argv[1])
