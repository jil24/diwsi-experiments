# this merely exposes the simplestage interface to python. It doesn't handle any abstraction or translation between physical units and steps. It just sends commands and waits for responses

import serial




class SimpleStage(object):
  def __init__(self, device_path):
    # hardcoded parameters for simplestage running on the arduino nano:
    self.serial_params = {
      'baudrate':115200,
      'bytesize':8,
      'parity':'N',
      'stopbits':1,
      'timeout':5,
      'xonxoff':0,
      'rtscts':0
    }
    
    self.ser = serial.Serial(device_path, **self.serial_params)
    if ser.readline().decode("ASCII").strip() != "SIMPLESTAGE READY":
      raise IOError("Did not receive expected SimpleStage bootup message")
    
  def report(self):
    # this should return within the timeout period
    ser.write(b'REPORT\n')
    report_text = ser.readline().decode("ASCII").strip()
    return report_text