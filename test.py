from realsense2 import StreamInfo as sif, RealSense2 as rs2
import threading
import time

_color = sif('color', 640, 480, 'bgr8', 30)
_depth = sif('depth', 640, 480, 'z16', 30)

rsObj = rs2([_color.streamInfo()])   #initial configuration is _color

time.sleep(1)

threading.Thread(target=rsObj.updateConfig, args=(([_depth.streamInfo()]),)).start()

time.sleep(1)

#after update, _depth configuration
rsObj.capture()
print(rsObj.depth_frame)

