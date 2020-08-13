import pyrealsense2 as rs
import numpy as np
import cv2
import os
import pandas as pd

class StreamInfo:
    def __init__(self, _streamType, _w, _h, _format, _fps):
        self.streamType = _streamType
        self.width = _w
        self.height = _h
        self.format = _format
        self.frameRate = _fps

    def getStreamInfo(self):
        if self.streamType == 'color':
            type = rs.stream.color
        elif self.streamType == 'depth':
            type = rs.stream.depth
        else:
            type = None

        if self.format == 'bgr8':
            data_format = rs.format.bgr8
        elif self.format == 'z16':
            data_format = rs.format.z16
        else:
            type = None

        streamInfo = {'streamType' : type, 'width' : self.width, 'height' : self.height,
                      'format' : data_format, 'frameRate' : self.frameRate}

        return streamInfo

class RealSense2:
    def __init__(self, _recordFilePath, _streamInfo):
        self.streamInfo = _streamInfo
        self.recordFilePath = _recordFilePath

    def capture(self):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(self.streamInfo['streamType'], self.streamInfo['width'],
                             self.streamInfo['height'], self.streamInfo['format'],
                             self.streamInfo['frameRate'])

        pipeline.start(config)
        try:
            colorizer = rs.colorizer()
            while True:
                frames = pipeline.wait_for_frames()

                if self.streamInfo['streamType'] == rs.stream.color:
                    color_frame = frames.get_color_frame()
                    color_image = np.asanyarray(color_frame.get_data())
                    
                    cv2.imshow('Color image', color_image)
                    k = cv2.waitKey(1) & 0xFF
                    if k == ord('q'):
                        cv2.imwrite(self.recordFilePath, color_image)
                        cv2.destroyAllWindows()
                        break

                else:
                    depth_frame = frames.get_depth_frame()
                    depth_image = np.asanyarray(depth_frame.get_data())
                    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                    # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                    # depth_frame = frames.get_depth_frame()
                    # depth_color_frame = colorizer.colorize(depth_frame)
                    # depth_image = np.asanyarray(depth_color_frame.get_data())

                    cv2.imshow('Depth image', depth_colormap)
                    # df = pd.DataFrame(data=depth_image)
                    k = cv2.waitKey(1) & 0xFF
                    if k == ord('q'):
                        cv2.imwrite(self.recordFilePath, depth_colormap)
                        # df.to_csv('depth_data.csv', index=False)
                        cv2.destroyAllWindows()
                        break
                    # cv2.destroyAllWindows()


        finally:
            pipeline.stop()

    def record(self, record_time):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_record_to_file(self.recordFilePath)
        config.enable_stream(self.streamInfo['streamType'], self.streamInfo['width'],
                             self.streamInfo['height'], self.streamInfo['format'],
                             self.streamInfo['frameRate'])

        pipeline.start(config)
        t1 = cv2.getTickCount()
        try:
            while True:
                frames = pipeline.wait_for_frames()

                if self.streamInfo['streamType'] == rs.stream.color:
                    color_frame = frames.get_color_frame()
                    color_image = np.asanyarray(color_frame.get_data())

                    cv2.imshow('Color image', color_image)
                    cv2.waitKey(1)
                    t2 = cv2.getTickCount()
                    if (t2 - t1)/cv2.getTickFrequency() > record_time:
                        break

                else:
                    depth_frame = frames.get_depth_frame()
                    depth_image = np.asanyarray(depth_frame.get_data())
                    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                    cv2.imshow('Depth image', depth_colormap)
                    print(depth_image)
                    cv2.waitKey(1)
                    t2 = cv2.getTickCount()
                    if (t2 - t1) / cv2.getTickFrequency() > record_time:
                        break

        finally:
            pipeline.stop()

    def displayRecordData(self):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_device_from_file(self.recordFilePath, repeat_playback=False)
        config.enable_stream(self.streamInfo['streamType'], self.streamInfo['width'],
                             self.streamInfo['height'], self.streamInfo['format'],
                             self.streamInfo['frameRate'])

        pipeline.start(config)

        try:
            colorizer = rs.colorizer()
            while True:
                frames = pipeline.wait_for_frames()

                if self.streamInfo['streamType'] == rs.stream.color:
                    color_frame = frames.get_color_frame()
                    color_image = np.asanyarray(color_frame.get_data())

                    cv2.imshow('Color image', color_image)
                    k = cv2.waitKey(1) & 0xFF
                    if k == ord('q'):
                        break

                else:
                    depth_frame = frames.get_depth_frame()
                    depth_color_frame = colorizer.colorize(depth_frame)
                    depth_image = np.asanyarray(depth_color_frame.get_data())

                    # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                    # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

                    cv2.imshow('Depth image', depth_image)
                    k = cv2.waitKey(1) & 0xFF
                    if k == ord('q'):
                        break
        finally:
            pipeline.stop()





