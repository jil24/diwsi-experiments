from diwsi.simplestage import SimpleStage
from diwsi.stage_xyz import Stage_XYZ
x = SimpleStage("/dev/ttyUSB0")
y = Stage_XYZ(x)
y.home()
