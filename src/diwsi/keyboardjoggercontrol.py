from sshkeyboard import listen_keyboard

class KeyboardJoggerControl(object):
  def __init__(self,
  
  stage_control_object,
  
  xy_small_jog = 0.05,
  xy_medium_jog = 0.1,
  xy_large_jog = 0.5,
  z_small_jog = 0.0025,
  z_medium_jog = 0.01,
  z_large_jog = 0.1,
  up_key = '8',
  down_key = '2',
  right_key = '6',
  left_key = '4',
  z_up_key = '9',
  z_down_key = '3',
  switch_small_key = '-',
  switch_medium_key = '+',
  switch_large_key = 'enter'
  ):
    # set attributes from invocation
    for key in list(locals().keys()):
      setattr(self, key, locals().get(key))
  
  def press(self, key):
      if key in self.lookups.keys():
        self.lookups[key]()
  
  def setmode(self, mode):
    self.mode = mode
    print("mode now set to {}".format(mode))
    
  def xy(self, x, y):
    if self.mode == "small":
      self.stage_control_object.relative_xy(x*self.xy_small_jog,y*self.xy_small_jog)
    elif self.mode == "medium":
      self.stage_control_object.relative_xy(x*self.xy_medium_jog,y*self.xy_medium_jog)
    else:
      self.stage_control_object.relative_xy(x*self.xy_large_jog,y*self.xy_large_jog)

  def z(self, z):
    if self.mode == "small":
      self.stage_control_object.relative_z(z*self.z_small_jog)
    elif self.mode == "medium":
      self.stage_control_object.relative_z(z*self.z_medium_jog)
    else:
      self.stage_control_object.relative_z(z*self.z_large_jog)
      

  def begin(self):
    self.mode = "medium"
    
    self.lookups = {
      self.up_key: lambda : self.xy(0,1),
      self.down_key: lambda : self.xy(0,-1),
      self.right_key: lambda : self.xy(1,0),
      self.left_key: lambda : self.xy(-1,0),
      self.z_up_key: lambda : self.z(1),
      self.z_down_key: lambda : self.z(-1),
      self.switch_small_key: lambda: self.setmode("small"),
      self.switch_medium_key: lambda: self.setmode("medium"),
      self.switch_large_key: lambda: self.setmode("large")
    }
    
    listen_keyboard(
      on_press=self.press,
      #on_release=release,
      delay_second_char = 0.05,
      sequential=True,
      )