#!/usr/bin/env python

import sys

from hamradio import HamRadio

def main(argv=None):
    hamradio = HamRadio()
    hamradio.RunFromArgs(argv)
    return

if __name__ == "__main__":
    main(sys.argv)