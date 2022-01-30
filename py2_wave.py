import binascii

#Little endian, 16-bit 2's complement
wave_points = [0x0010, 0x0020, 0x0030, 0x0040, 0x0050, 0x0060, 0x0070, 0xff7f]

def create_wave_file():
  """create a file"""
  f = open("wave1.bin", "wb")
  for a in wave_points:
    b = hex(a)
    b = b[2:]
    len_b = len(b)
    if (0 == len_b):
      b = '0000'
    elif (1 == len_b):
      b = '000' + b
    elif (2 == len_b):
      b = '00' + b
    elif (3 == len_b):
      b = '0' + b
    c = binascii.a2b_hex(b)
    #Hexadecimal integer to ASCii encoded string
    f.write(c)
  f.close()

def print_wave_data():
  """send wave1.bin to the device"""
  f = open("wave1.bin", "rb")
  data = f.read()
  f.close()
  print("C1:WVDT WVNM,wave1,FREQ,2000.0,AMPL,4.0,OFST,0.0,PHASE,0.0,WAVEDATA,%s"  %   (data))

create_wave_file()
print_wave_data()
