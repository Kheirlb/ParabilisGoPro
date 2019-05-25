import time
from goprocam import GoProCamera, constants
gp1 = GoProCamera.GoPro()

gp1.shutter(constants.stop)

print("End of Script")