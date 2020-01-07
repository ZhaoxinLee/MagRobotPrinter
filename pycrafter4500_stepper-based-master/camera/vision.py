import numpy as np
import cv2, sys, os, time
from objectDetection import drawContour

class Vision(object):
    def __init__(self,mode):
        if mode == 'Video':
            self.mode = mode
            self.cap = cv2.VideoCapture("Frog.avi")
            self.frameCounter = 0
        else:
            self.mode = mode
            self.cap = cv2.VideoCapture(0)
        cv2.namedWindow(self.windowName(),16)
        cv2.moveWindow(self.windowName(), 0, 100)
        cv2.resizeWindow(self.windowName(), 640,512)

        self._isGrayscale = False
        self._isThresholdRunning = False
        self._isObjectDetectionRunning = False
        self.threshold = None
        self.maxval = None
        self.cnt_routing = np.zeros((0,2),dtype=np.uint8)
        self.state = 0
        self.firstFrameNo = None
        self.snapshotState = False
        self.videoWritingState = False

    def updateFrame(self):
        if self.mode == 'Video':
            ret, frame = self.cap.read()

            self.frameCounter += 1
            #If the last frame is reached, reset the capture and the frame_counter
            if self.frameCounter == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.frameCounter = 0 #Or whatever as long as it is the same as next line
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            if self.isObjectDetectionRunning():
                # to prevent overflow of cnt_routing, we just capture the contour for one video cycle
                if self.state == 0:
                    self.firstFrameNo = self.frameCounter
                    self.state = 1
                # if loop back to the n-1 frame, append no more, special case for the frame 1
                if self.firstFrameNo == 1:
                    if self.frameCounter == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                        self.state = 2
                else:
                    if self.frameCounter == self.firstFrameNo - 1:
                        self.state = 2

                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                filteredFrame = self.runThreshold(grayFrame)
                processedFrame, cnts = drawContour(filteredFrame,frame)
                if self.state == 1:
                    self.cnt_routing = np.append(self.cnt_routing, cnts, axis=0)
                processedFrame[self.cnt_routing[:,1],self.cnt_routing[:,0]] = (0, 255, 0)
                cv2.imshow(self.windowName(),processedFrame)
                shownFrame = processedFrame
            elif self.isThresholdRunning():
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                filteredFrame = self.runThreshold(grayFrame)
                cv2.imshow(self.windowName(),filteredFrame)
                shownFrame = filteredFrame
            elif self.isGrayscale():
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow(self.windowName(),grayFrame)
                shownFrame = grayFrame
            else:
                cv2.imshow(self.windowName(),frame)
                shownFrame = frame
            if self.snapshotState:
                timestr = time.strftime("%Y%m%d%H%M%S")
                cv2.imwrite(os.getcwd()+'/snapshot/snapshot_'+timestr+'.png',shownFrame)
                self.snapshotState = False
            if self.videoWritingState:
                self.videoWriter.write(shownFrame)

        else:
            ret, frame = self.cap.read()
            if self.isObjectDetectionRunning():
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                filteredFrame = self.runThreshold(grayFrame)
                processedFrame, cnts = drawContour(filteredFrame,frame)
                if self.state == 0:
                    self.cnt_routing = np.append(self.cnt_routing, cnts, axis=0)
                processedFrame[self.cnt_routing[:,1],self.cnt_routing[:,0]] = (0, 255, 0)
                cv2.imshow(self.windowName(),processedFrame)
                shownFrame = processedFrame
            elif self.isThresholdRunning():
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                filteredFrame = self.runThreshold(grayFrame)
                cv2.imshow(self.windowName(),filteredFrame)
                shownFrame = filteredFrame
            elif self.isGrayscale():
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow(self.windowName(),grayFrame)
                shownFrame = grayFrame
            else:
                cv2.imshow(self.windowName(),frame)
                shownFrame = frame
            if self.snapshotState:
                timestr = time.strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(os.getcwd()+'/snapshot/snapshot_'+timestr+'.png',shownFrame)
                self.snapshotState = False
            if self.videoWritingState:
                self.videoWriter.write(shownFrame)

    def windowName(self):
        return 'Camera'

    def getFrameRate(self):
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        return(self.fps)

    def isGrayscale(self):
        return self._isGrayscale

    def isThresholdRunning(self):
        return self._isThresholdRunning

    def isObjectDetectionRunning(self):
        return self._isObjectDetectionRunning

    def setOriginal(self):
        self._isGrayscale = False
        self._isThresholdRunning = False
        self._isObjectDetectionRunning = False
        self.cnt_routing = np.zeros((0,2),dtype=np.uint8)
        self.state = 0
        self.firstFrameNo = None

    def setGrayscale(self):
        self._isGrayscale = True
        self._isThresholdRunning = False
        self._isObjectDetectionRunning = False

    def setThreshold(self,threshold,maxval):
        self.threshold = threshold
        self.maxval = maxval
        self._isThresholdRunning = True
        self._isObjectDetectionRunning = False

    def setObjectDetection(self,threshold,maxval):
        self.threshold = threshold
        self.maxval = maxval
        self._isObjectDetectionRunning = True

    def susObjectDetection(self):
        self.state = 2

    def runThreshold(self,inputImage):
        _, ret = cv2.threshold(inputImage,self.threshold,self.maxval,cv2.THRESH_BINARY)
        return ret

    def setSnapshot(self):
        self.snapshotState = True

    #==============================================================================================
    # Video recording
    #==============================================================================================

    def startRecording(self,fileName):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.videoWriter = cv2.VideoWriter(os.getcwd()+'/video/'+fileName+'_'+timestr+'.avi',fourcc=cv2.VideoWriter_fourcc(*'MJPG'),fps=self.cap.get(cv2.CAP_PROP_FPS),\
                            frameSize=(int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),isColor=True)
        self.setVideoWritingEnabled(True)
        print('Start recording '+fileName+'_'+timestr+'.avi...')

    def stopRecording(self):
        self.setVideoWritingEnabled(False)
        self.videoWriter.release()
        print('Stop recording.')

    def setVideoWritingEnabled(self,state):
        self.videoWritingState = state
