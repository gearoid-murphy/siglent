#!/usr/bin/env python3

import numpy as np
import pyvisa as visa
import struct
import matplotlib.pyplot as plt
import binascii

import logging
import sys

# visa.log_to_screen()
resources = visa.ResourceManager('@py')
# resources.list_resources()
# device = resources.open_resource('USB0::62700::4355::SDG1XCAX4R1193::0::INSTR',
#                                  write_termination='\n',
#                                  read_termination='\n',
#                                  query_delay=0.25)

# http://zone.ni.com/reference/en-XX/help/371361J-01/lvinstio/visa_resource_name_generic/
device = resources.open_resource('TCPIP::192.168.86.32::INSTR', write_termination='\n', read_termination='\n')

# Default timeout is 2000 ms, which is too long, so make shorter
device.timeout = 500  # in milliseconds

# Query all basic wave parameters
# device.query('C1:BSWV?')

# Set the frequency to 2khz
# device.write('C1:BSWV FRQ,2000')

# Set the voltage offset
# device.write('C1:BSWV OFST,1.1')

# Index is how built-in arb waves are referenced
# device.write('C1:ARWV INDEX,24')

# Name is how user defined waves are referenced
# device.write("C1:ARWV NAME,wave1")

# Reading the uploaded data
# device.write('WVDT? USER,wave1'); response = device.read_raw()
#

sequence_length = 16384
# max_value = 32767
max_value = 32767


def GenPulseSequence(num_pulses, pulse_width):
  waveform = np.ones(sequence_length)
  for i in range(num_pulses):
    offset = i * (pulse_width * 2)
    for j in range(pulse_width):
      waveform[offset + j] = max_value

  return waveform.astype(np.int16)


def GenSinePulse(frequency, pulse_width):
  step_size = np.pi * 2.0 * frequency / pulse_width
  time = np.arange(0, np.pi * 2.0 * frequency, step_size)
  amplitude = np.sin(time) * max_value
  waveform = np.full(2048, 2048)
  waveform[0:pulse_width] = amplitude
  return waveform.astype(np.int16)


def SendWave(num_points, multipler=1):
  # device.write(f"C1:WVDT WVNM,wave1,FREQ,2000.0,AMPL,5.0,OFST,0.0,PHASE,0.0,WAVEDATA,0000fff1")
  # device.write(f"C1:WVDT WVNM,wave1,WAVEDATA,0000fff1")
  # The byte encoding is litte-endian
  # device.write_raw(b"C1:WVDT WVNM,wave1,WAVEDATA,\x00\x00\x00\x80\x00\x00\xff\x7f")
  wave_packet = []
  # Format the range to avoid the write termination character
  for k in range(multipler):
    for i in range(11, 11 + num_points):
      wave_packet.append(bytes([i]))

  # print(b"".join(wave_packet).hex())
  # device.write_raw(b"C1:WVDT WVNM,wave1,WAVEDATA," +
  #                  b"".join(wave_packet) +
  #                  str.encode(device.write_termination))
  device.write_binary_values("C1:WVDT WVNM,wave1,WAVEDATA,", b"".join(wave_packet))

  # device.write('C1:ARWV NAME,wave1')

import IPython
IPython.embed()
