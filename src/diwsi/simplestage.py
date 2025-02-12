# this merely exposes the simplestage interface to python. It doesn't handle any abstraction, relative movements, or translation between physical units and steps. It just sends commands and waits for responses

import serial

class SimpleStage(object):
  def __init__(self, device_path):
    # hardcoded parameters for simplestage running on the arduino nano:
    serial_params = {
      'baudrate':115200,
      'bytesize':8,
      'parity':'N',
      'stopbits':1,
      'timeout':5,
      'xonxoff':0,
      'rtscts':0
    }
    
    self.ser = serial.Serial(device_path, **serial_params)
    response = self.ser.readline().decode("ASCII").strip()
    if response != "SIMPLESTAGE READY":
      raise IOError("Did not receive expected SimpleStage bootup message - Instead received {}".format(response))
    self.update_attr()
    
  def report(self):
    # this should return within the timeout period
    self.ser.write(b'REPORT\n')
    report_text = self.ser.readline().decode("ASCII").strip()
    report_dict = {param.split(":")[0].lower(): int(param.split(":")[1]) for param in report_text.split(" ")}
    return report_dict
    
  def update_attr(self):
    # fetch and update everything
    for key, value in self.report().items():
      setattr(self, key, value)
  
  def __long_command(self, command, successresponse, maxtimeouts=30):
    self.ser.write('{}\n'.format(command).encode("ASCII"))
    for i in range(maxtimeouts):
      response = self.ser.readline().decode("ASCII").strip()
      if response == successresponse:
        self.update_attr()
        return None
      elif response != "":
        raise IOError("Did not receive expected response - Instead received {}".format(response))
    raise IOError("Did not receive expected response - timed out")
  
  def set_xyspeed(self, speed):
    # this should return within the timeout period
    self.ser.write('XYSPEED {}\n'.format(speed).encode("ASCII"))
    response = self.ser.readline().decode("ASCII").strip()
    if response != "XYSPEED {} DONE".format(speed):
      raise IOError("Did not receive expected response - Instead received {}".format(response))
    self.update_attr()

  def set_zspeed(self, speed):
    # this should return within the timeout period
    self.ser.write('ZSPEED {}\n'.format(speed).encode("ASCII"))
    response = self.ser.readline().decode("ASCII").strip()
    if response != "ZSPEED {} DONE".format(speed):
      raise IOError("Did not receive expected response - Instead received {}".format(response))
    self.update_attr()
      
  def set_accel(self, accel):
    # this should return within the timeout period
    self.ser.write('ACCEL {}\n'.format(accel).encode("ASCII"))
    response = self.ser.readline().decode("ASCII").strip()
    if response != "ACCEL {} DONE".format(accel):
      raise IOError("Did not receive expected response - Instead received {}".format(response))
    self.update_attr()
  
  def set_led(self, led):
    # this should return within the timeout period
    self.ser.write('LED {}\n'.format(led).encode("ASCII"))
    response = self.ser.readline().decode("ASCII").strip()
    if response != "LED {} DONE".format(led):
      raise IOError("Did not receive expected response - Instead received {}".format(response))
    self.update_attr()
    
  def move_xy(self, x, y):
    self.__long_command(command = "XY {} {}".format(x,y),
                        successresponse = "XY {} {} DONE".format(x,y))

  def move_z(self, z):
    self.__long_command(command = "Z {}".format(z),
                        successresponse = "Z {} DONE".format(z))

  def home(self, xmax, ymax, zmax):
    maxtimeouts=30
    successresponse="LIMITS: "
    self.ser.write('HOME {} {} {}\n'.format(xmax, ymax, zmax).encode("ASCII"))
    for i in range(maxtimeouts):
      response = self.ser.readline().decode("ASCII").strip()
      if response.startswith(successresponse):
        # there's no need to parse the response since we get the limits with the attr_update call
        self.update_attr()
        return None
      elif response != "":
        raise IOError("Did not receive expected response - Instead received {}".format(response))
    raise IOError("Did not receive expected response - timed out")