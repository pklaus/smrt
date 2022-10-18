#!/usr/bin/env python3
import logging
def loglevel(x):
    try:
        return getattr(logging, x.upper())
    except AttributeError:
        raise argparse.ArgumentError('Select a proper loglevel')

if __name__ == '__main__':
    pass
