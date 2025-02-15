import logging
from diwsi.simplestage import SimpleStage

logger = logging.getLogger(__name__)

class SoftLimitExceeded(Exception):
    '''An operation that would exceed soft limits was requested'''




class StageXYZ(object):
  # conversion methods
  def mm_to_microsteps(self, mm, axis):
    # will round to nearest integer number of steps
    leadscrew_physical_lead_mm = getattr(self, "axis_{}_leadscrew_physical_lead_mm".format(axis))
    stepper_fullsteps_per_rev = getattr(self, "axis_{}_stepper_fullsteps_per_rev".format(axis))
    microstep_multiplier = getattr(self, "axis_{}_microstep_multiplier".format(axis))
    return round((float(mm) / leadscrew_physical_lead_mm) * stepper_fullsteps_per_rev * microstep_multiplier)      
      
  def microsteps_to_mm(self, microsteps, axis):
    leadscrew_physical_lead_mm = getattr(self, "axis_{}_leadscrew_physical_lead_mm".format(axis))
    stepper_fullsteps_per_rev = getattr(self, "axis_{}_stepper_fullsteps_per_rev".format(axis))
    microstep_multiplier = getattr(self, "axis_{}_microstep_multiplier".format(axis))
    return ((float(microsteps)/microstep_multiplier)/stepper_fullsteps_per_rev)*leadscrew_physical_lead_mm
    
  def update_position_from_device(self):
    setattr(self, 'position_x', self.microsteps_to_mm(self.device_object.x,'x'))
    setattr(self, 'position_y', self.microsteps_to_mm(self.device_object.y,'y'))
    setattr(self, 'position_z', self.microsteps_to_mm(self.device_object.z,'z'))    
  
  def update_limits_from_device(self):
    setattr(self, 'axis_x_hard_limit_position', self.microsteps_to_mm(self.device_object.xlimit,'x'))
    setattr(self, 'axis_y_hard_limit_position', self.microsteps_to_mm(self.device_object.ylimit,'y'))
    setattr(self, 'axis_z_hard_limit_position', self.microsteps_to_mm(self.device_object.zlimit,'z'))
  
  def update_speeds_from_device(self):
    setattr(self, 'axis_x_topspeed_mm_per_sec', self.microsteps_to_mm(self.device_object.xyspeed,'x'))
    setattr(self, 'axis_z_topspeed_mm_per_sec', self.microsteps_to_mm(self.device_object.zspeed,'z'))
    
  def update_accel_from_device(self):
    setattr(self, 'axis_x_accel_mm_per_sec_sq', self.microsteps_to_mm(self.device_object.accel,'x'))
  
  def set_soft_limits(self):
    distance_from_x_hard_limit = (self.axis_x_hard_limit_position*(1-self.axis_x_soft_limit_fraction))/2
    distance_from_y_hard_limit = (self.axis_y_hard_limit_position*(1-self.axis_y_soft_limit_fraction))/2
    distance_from_z_hard_limit = (self.axis_z_hard_limit_position*(1-self.axis_z_soft_limit_fraction))/2
    setattr(self, 'axis_x_soft_limits', [distance_from_x_hard_limit,self.axis_x_hard_limit_position-distance_from_x_hard_limit])
    setattr(self, 'axis_y_soft_limits', [distance_from_y_hard_limit,self.axis_y_hard_limit_position-distance_from_y_hard_limit])
    setattr(self, 'axis_z_soft_limits', [distance_from_z_hard_limit,self.axis_z_hard_limit_position-distance_from_z_hard_limit])
    self.axis_x_soft_limits.sort()
    self.axis_y_soft_limits.sort()
    self.axis_z_soft_limits.sort()

  def set_x_topspeed_mm_per_sec(self, axis_x_topspeed_mm_per_sec):
    # y topspeed is implied but not set explicitly
    self.device_object.set_xyspeed(self.mm_to_microsteps(axis_x_topspeed_mm_per_sec,'x'))
    setattr(self, 'axis_x_topspeed_mm_per_sec', self.microsteps_to_mm(self.device_object.xyspeed,'x'))
    
  def set_z_topspeed_mm_per_sec(self, axis_z_topspeed_mm_per_sec):
    self.device_object.set_zspeed(self.mm_to_microsteps(axis_z_topspeed_mm_per_sec,'z'))
    setattr(self, 'axis_z_topspeed_mm_per_sec', self.microsteps_to_mm(self.device_object.zspeed,'z'))

  def set_x_accel_mm_per_sec_sq(self, axis_x_accel_mm_per_sec_sq):
    self.device_object.set_accel(self.mm_to_microsteps(axis_x_accel_mm_per_sec_sq,'x'))
    self.update_accel_from_device()

  # initialization - remember that y speed isn't defined. since Y axis can have different leadscrew geometry from X axis we only define X speed. Accel is global
  def __init__(self, 
  
  device_object,
  
  axis_x_leadscrew_physical_lead_mm = 1,
  axis_x_stepper_fullsteps_per_rev = 200,
  axis_x_microstep_multiplier = 8,
  axis_x_soft_limit_fraction = 0.98,
  axis_x_maximum_travel_mm = 150,

  axis_y_leadscrew_physical_lead_mm = 1,
  axis_y_stepper_fullsteps_per_rev = 200,
  axis_y_microstep_multiplier = 8,
  axis_y_soft_limit_fraction = 0.98,
  axis_y_maximum_travel_mm = 100,
  
  axis_z_leadscrew_physical_lead_mm = 0.3,
  axis_z_stepper_fullsteps_per_rev = 200,
  axis_z_microstep_multiplier = 8,
  axis_z_soft_limit_fraction = 0.98,
  axis_z_maximum_travel_mm = 100,

  axis_x_topspeed_mm_per_sec = 5,
  axis_x_accel_mm_per_sec_sq = 5,
  axis_z_topspeed_mm_per_sec = 2
  ):
    if type(device_object) is not SimpleStage:
      raise NotImplementedError("only simplestage has been implemented as a device module so far")
    self.device_object = device_object
    
    # set axis attributes from invocation
    for key in list(locals().keys()):
      if key.startswith("axis_"):
        setattr(self, key, locals().get(key))
        
    # enumerate position and limits from the device object, converting from microsteps to mm
    self.update_position_from_device()
    self.update_limits_from_device()
    if (self.axis_x_hard_limit_position == 0) and (self.axis_y_hard_limit_position == 0) and (self.axis_z_hard_limit_position == 0):
      setattr(self, "home_performed", False)
    else:
      setattr(self, "home_performed", True)
      self.set_soft_limits()
      
    # convert and pass speed and acceleration settings on to the device_object
    self.set_x_topspeed_mm_per_sec(axis_x_topspeed_mm_per_sec)
    self.set_z_topspeed_mm_per_sec(axis_z_topspeed_mm_per_sec)
    self.set_x_accel_mm_per_sec_sq(axis_x_accel_mm_per_sec_sq)
    self.update_speeds_from_device()
    self.update_accel_from_device()
    
  # absolute xy moves
  def to_xy(self,x,y):
    if not self.home_performed:
      logger.warning('stage has not been homed - soft limits are not set!')
    else:
      if x < self.axis_x_soft_limits[0] or x > self.axis_x_soft_limits[1] or y < self.axis_y_soft_limits[0] or y > self.axis_y_soft_limits[1]:
        raise SoftLimitExceeded
    self.device_object.move_xy(
      self.mm_to_microsteps(x,'x'),
      self.mm_to_microsteps(y,'y')
      )
    self.update_position_from_device()
      
  # absolute z moves
  def to_z(self,z):
    if not self.home_performed:
      logger.warning('stage has not been homed - soft limits are not set!')
    else:
      if z < self.axis_z_soft_limits[0] or z > self.axis_z_soft_limits[1]:
        raise SoftLimitExceeded
    self.device_object.move_z(self.mm_to_microsteps(z,'z'))
    self.update_position_from_device()
    
  # relative xy moves
  def relative_xy(self,relative_x,relative_y):
    x = self.position_x + relative_x
    y = self.position_y + relative_y
    if not self.home_performed:
      logger.warning('stage has not been homed - soft limits are not set!')
    else:
      if x < self.axis_x_soft_limits[0] or x > self.axis_x_soft_limits[1] or y < self.axis_y_soft_limits[0] or y > self.axis_y_soft_limits[1]:
        raise SoftLimitExceeded
    self.device_object.move_xy(
      self.mm_to_microsteps(x,'x'),
      self.mm_to_microsteps(y,'y')
      )
    self.update_position_from_device()

  # relative z moves
  def relative_z(self,relative_z):
    z = self.position_z + relative_z
    if not self.home_performed:
      logger.warning('stage has not been homed - soft limits are not set!')
    else:
      if z < self.axis_z_soft_limits[0] or z > self.axis_z_soft_limits[1]:
        raise SoftLimitExceeded
    self.device_object.move_z(self.mm_to_microsteps(z,'z'))
    self.update_position_from_device()
  
  # homing
  def home(self):
    x = self.mm_to_microsteps(self.axis_x_maximum_travel_mm, 'x')
    y = self.mm_to_microsteps(self.axis_y_maximum_travel_mm, 'y')
    z = self.mm_to_microsteps(self.axis_z_maximum_travel_mm, 'z')
    self.device_object.home(x,y,z)
    self.home_performed = True
    self.update_position_from_device()
    self.update_limits_from_device()
    self.set_soft_limits()
