import numpy as np
import cv2, math

def detectBiggestContour(imageFiltered,imageOriginal):
    nOfSamples = 4
    contours, hierarchy = cv2.findContours(imageFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:nOfSamples]
    if len(cnts) > 0:
        targetCnt = cnts[0] # cnt[0] is the edge of the screen
        rect = cv2.minAreaRect(targetCnt) # (x,y)(w,h)theta
        box = np.int0(cv2.boxPoints(rect)) # vertices of the bounding rect
        center = np.int0(np.sum(box, axis=0)/4) # [centerX, centerY] dataType: int
        agent.set(center[0],center[1],rect[2]) # update the position of the agnet
        cv2.drawContours(imageOriginal,[box],0,(0,255,0), 3) # draw boundingRect on the original image
        #print(rect[2])
    return imageOriginal


def drawContour(ff,frame):
    nOfSamples = 4
    #print(ff.shape)
    contours, _ = cv2.findContours(ff, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = np.zeros((0,2),dtype=np.uint8)
    # print(np.array(np.array(contours))[0])
    if contours != []:
        cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:nOfSamples]
        # cnts = np.squeeze(cnts,axis=0)
        cnts = np.squeeze(cnts[0],axis=1)
        # print(cnts[0][0])
        # print(cnts[0][1])
        # print(cnts.shape)
        # print(cnts[:,0])
        # print(np.array(cnts).shape)
        # contour_routing = np.append(contour_routing, cnts[0], axis=0)
        # contour_routing.append(cnts[0])
        # print(contour_routing)
        #print(np.squeeze(np.array(contour_routing),axis=0).shape)
    # print(contour_routing)
        # contour_routing = np.array(contour_routing)
    # cv2.drawContours(frame, np.array([[[500,500],[501,501]]]), -1, (0, 255, 0), thickness=10)
    # if contour_routing != []:
        # cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=-1)
    return frame, cnts
