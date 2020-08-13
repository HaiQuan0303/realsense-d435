from realsense2 import RealSense2 as rs2, StreamInfo as sif

info = sif('depth', 640, 480, 'z16', 30)
streamInfo = info.getStreamInfo()
path = './video/video1.bag'
color_image = rs2(path, streamInfo)
color_image.displayRecordData()