from diwsi import simplestage
from diwsi import stagexyz
from diwsi import keyboardjoggercontrol

# factory function for each module type

def ControllerDeviceModule(type,**kwargs):
  if type == "SimpleStage":
    return simplestage.SimpleStage(**kwargs)
  else:
    raise NotImplementedError("no module for {}".format(type))


def StageControlModule(type,**kwargs):
  if type == "StageXYZ":
    return stagexyz.StageXYZ(**kwargs)
  else:
    raise NotImplementedError("no module for {}".format(type))


def InterfaceModule(type,**kwargs):
  if type == "KeyboardJoggerControl":
    return keyboardjoggercontrol.KeyboardJoggerControl(**kwargs)
  else:
    raise NotImplementedError("no module for {}".format(type))