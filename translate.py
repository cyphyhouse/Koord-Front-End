#!/usr/bin/env python
import sys

from KoordFE.parser import mycompiler

def main(argv):
    filename = argv[1]
    mycompiler().compile(filename)

if __name__ == "__main__":
    main(sys.argv)
