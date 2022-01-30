#!/usr/bin/env python3

import numpy as np
import pyvisa as visa
import struct
import matplotlib.pyplot as plt

resources = visa.ResourceManager('@py')
device = resources.open_resource(
    'USB0::62700::60986::SDS1MEBC3R1385::0::INSTR',
    write_termination='\n',
    query_delay=0.25)

device.write('WFSU SP,0,NP,0,F,0')
# device.write('WFSU TYPE, 0') # Just what's on the device display
# device.write('WFSU TYPE, 1') # All memory points

# Default timeout is 2000 ms, which is too long, so make shorter
device.timeout = 500  # in milliseconds

# Print settings read from device
# print(device.query("SARA?"))  # Sampling Rate
# print(device.query("SANU? C1"))  # Sample size for channel 1
# print(device.query("TDIV?"))  # Time base
# print(device.query("TRDL?"))  # Time delay
# print(device.query("TRSE?"))  # Trigger Condition, e.g. Interval
# print(device.query("C1:TRLV?"))  # Trigger Level
# print(device.query("TRMD?"))  # Trigger Sweep Mode
# print(device.query("C1:TRCP?"))  # Trigger Coupling for channel 1
# print(device.query("C1:TRLV2?"))  # Trigger Level 2

# In [54]: device.query('VDIV?')
# Out[54]: 'C1:VDIV 1.00E-02V\n\x00\x00'


def GetWaveform():
  device.write('C1:WF? DAT2')
  response = device.read_raw()
  wave = response[21:-3]
  num_points = len(wave)
  integers = np.array(struct.unpack('b'*num_points, wave))
  return integers

wave = GetWaveform()

import IPython
IPython.embed()




