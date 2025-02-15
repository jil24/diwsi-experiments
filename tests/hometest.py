from diwsi.simplestage import SimpleStage
from diwsi.stagexyz import StageXYZ
x = SimpleStage("/dev/ttyUSB0")
y = StageXYZ(x)
y.home()
