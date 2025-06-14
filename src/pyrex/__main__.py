#!/usr/bin/env python3
"""Simplifies `xterm` color usage and management.
"""
##########################################################################################################################################################
# TESTS

def test():
  import doctest
  from . import __source__
  return doctest.testmod(__source__)

##########################################################################################################################################################

def main():
  import sys
  from . import Spectrum
  # Run tests
  if test().failed:
    sys.exit(1)
  # Run the Kaleidoscope
  if sys.argv[-1] == '-K':
    Spectrum.Kaleidoscope()
  # Print all colors
  else:
    print(Spectrum)
  sys.exit(0)

if __name__ == "__main__": main()

##########################################################################################################################################################
