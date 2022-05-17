#! /usr/bin/env python3

import sys
import signal
import logging
import argparse

parser = argparse.ArgumentParser(description=sys.argv[0])
parser.add_argument('-a', '--attempt', type=int, default=0, help='Attempt number')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(filename='./retry.log', format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger(sys.argv[0])
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

# print('foo')
# print('bar')
print('dpkg-sig')
log.info(f'Attempt #{args.attempt}')
# exit(1)
