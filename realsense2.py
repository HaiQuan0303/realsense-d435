import pyrealsense2 as rs
import numpy as np
import cv2
import threading


class StreamInfo:
    def __init__(self, _streamType, _w, _h, _format, _fps):
        self.streamType = _streamType
        self.width = _w
        self.height = _h
        self.format = _format
        self.frameRate = _fps

    def streamInfo(self):
        if self.streamType == 'color':
            type = rs.stream.color
            if self.format == 'bgr8':
                data_format = rs.format.bgr8
            else:
                return False

        elif self.streamType == 'depth':
            type = rs.stream.depth
            if self.format == 'z16':
                data_format = rs.format.z16
            else:
                return False

        else:
            return False

        streamInfo = {'streamType' : type, 'width' : self.width, 'height' : self.height,
                          'format' : data_format, 'frameRate' : self.frameRate}
        return streamInfo


class RealSense2:
    #Device serial number is '001622072448'
    def __init__(self, _streamInfos, _recordFilePath = 'record_bag_file.bag',  _devSerial = '001622072448'):
        self.streamInfos = _streamInfos
        self.recordFilePath = _recordFilePath
        self.devSerial = _devSerial
        self.isRecording = False
        self.color_frame = []
        self.depth_frame = []

        self._color_frame = []
        self._depth_frame = []

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(self.devSerial)

        self.release = False
        self.isUpdateConfig = False

        threading.Thread(target=self.record, name='record').start()


    def record(self):
        self.config.enable_record_to_file(self.recordFilePath)
        while True:
            types = []  #can be color, depth or both
            for streamInfo in self.streamInfos:
                self.config.enable_stream(streamInfo['streamType'], streamInfo['width'], streamInfo['height'],
                                          streamInfo['format'], streamInfo['frameRate'])
                types.append(streamInfo['streamType'])

            self.pipeline.start(self.config)
            while True:
                frames = self.pipeline.wait_for_frames()

                if rs.stream.color in types:
                    self._color_frame = frames.get_color_frame()

                if rs.stream.depth in types:
                    self._depth_frame = frames.get_depth_frame()

                if self.isUpdateConfig:
                    break
            # continue
            if self.release:
                self.pipeline.stop()
                break
            else:
                self.pipeline.stop()
                self.isUpdateConfig = False
                continue

    def capture(self):
        if self.isRecording:
            print('Device is busy')
            return False
        while True:
            if self._color_frame:
                self.color_frame = np.asanyarray(self._color_frame.get_data())
            if self._depth_frame:
                self.depth_frame = np.asanyarray(self._depth_frame.get_data())

            if (not self._color_frame) and (not self._depth_frame):
                continue

            break

        print('Succeed capture')
        return True

    def startRecording(self, record_time):
        print('Start record')
        self.isRecording = True
        t1 = cv2.getTickCount()

        while self.isRecording:

            if self._color_frame and self._depth_frame:
                color_frame = np.asanyarray(self._color_frame.get_data())
                depth_frame = np.asanyarray(self._depth_frame.get_data())

            elif self._color_frame:
                color_frame = np.asanyarray(self._color_frame.get_data())

            elif self._depth_frame:
                depth_frame = np.asanyarray(self._depth_frame.get_data())

            else:
                continue

            if (cv2.getTickCount() - t1)/cv2.getTickFrequency() > record_time:
                break

        print('End record')
        self.isRecording = False
        self.release = True

    def stopRecording(self):
        self.isRecording = False
        print('Stop record')

    def updateConfig(self, _streamInfos):
        self.isUpdateConfig = True
        self.streamInfos = _streamInfos
        print("Change configuration")




