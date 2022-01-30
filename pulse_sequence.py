#!/usr/bin/env python3

import numpy as np
import pyvisa as visa
import struct
import matplotlib.pyplot as plt
import binascii
import struct
import logging
import sys

# visa.log_to_screen()
resources = visa.ResourceManager('@py')
device = resources.open_resource('TCPIP::192.168.86.24::INSTR',
                                 write_termination='\n',
                                 read_termination='\n')
device.timeout = 500  # in milliseconds

max_sequence_length = 16384
bit_range = 16
value_range = (1 << (bit_range - 1)) - 1


def GenSquarePulse(num_cycles, cycle_width, amplitude):
  assert amplitude == +1.0 or amplitude == -1.0
  pulse_width = num_cycles * cycle_width
  assert pulse_width <= max_sequence_length
  waveform = np.zeros((max_sequence_length))
  for c in range(num_cycles):
    offset = c * cycle_width
    for i in range(cycle_width//2):
      waveform[offset + i] = amplitude
    for i in range(cycle_width//2, cycle_width):
      waveform[offset + i] = 0
  return waveform

def GenSinePulse(num_cycles, cycle_width):
  pulse_width = num_cycles * cycle_width
  assert pulse_width <= max_sequence_length
  step_size = (np.pi * 2.0 * num_cycles) / pulse_width
  time = np.arange(0, np.pi * 2.0 * num_cycles, step_size)
  amplitude = np.sin(time)
  waveform = np.zeros((max_sequence_length))
  waveform[0:pulse_width] = amplitude
  return waveform


def GenConstrainedSinePulse(num_cycles, cycle_width, voltage_range, amplitude,
                            offset):
  pulse_train_width = num_cycles * cycle_width
  assert pulse_train_width <= max_sequence_length
  step_size = (np.pi * 2.0 * num_cycles) / pulse_train_width
  time = np.arange(0, np.pi * 2.0 * num_cycles, step_size)
  pulse_train = np.sin(time)
  constrained_amplitude = amplitude / voltage_range
  pulse_train *= constrained_amplitude
  contrained_offset = offset / voltage_range
  pulse_train += contrained_offset
  waveform = np.zeros((max_sequence_length))
  waveform[0:pulse_train_width] = pulse_train
  return waveform


def EncodeWave(waveform):
  assert waveform.shape == (max_sequence_length,)
  encoded = []
  for v in waveform:
    assert v >= -1.0 and v <= 1.0
    tgt = int(round(v * value_range))
    encoded.append(struct.pack('<h', tgt))
  return b"".join(encoded)


def SendWave(waveform, frequency, amplitude):
  encoded = EncodeWave(waveform)
  device.write_raw(
      str.encode("C1:WVDT WVNM,wave1,"
                 f"FREQ,{frequency},"
                 f"AMPL,{amplitude},OFST,0,WAVEDATA,") + encoded)
  device.write('')
  device.write('C1:ARWV NAME,wave1')


def SendRamp(num_points):
  encoded = []
  step_size = (value_range * 2) // num_points
  for i in range(-value_range, +value_range, step_size):
    encoded.append(struct.pack('<h', i))
  encoded = b"".join(encoded)
  device.write_raw(b"C1:WVDT WVNM,wave1,WAVEDATA," + encoded)
  device.write('')
  device.write('C1:ARWV NAME,wave1')


import IPython
IPython.embed()
