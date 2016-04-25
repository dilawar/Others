
"""locate_mouse_substract_background.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh "
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"


import numpy as np
import cv2
import sys
import imageio
from image_analysis_submodule import contour_detector as cnt


def onmouse(event, x, y, flags, params):
    global current_frame_, bbox_
    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox_ = []
        bbox_.append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        bbox_.append((x, y))
        cv2.rectangle(current_frame_, bbox_[0], (x,y), 0,2)


def get_rectangle( frame ):
    global bbox_
    global current_frame_
    current_frame_ = frame.copy()
    title = "Bound head and press 'q' to quit."
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, onmouse)
    clone = frame.copy()
    while True:
        cv2.imshow(title, current_frame_)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            current_frame_ = clone.copy()
        elif key == ord("q"):
            break
    cv2.waitKey(1)
    cv2.destroyWindow( title )
    return bbox_

vid = imageio.get_reader( sys.argv[1] )

# take first frame of the video
numFrame = 900
firstFrame = vid.get_data( numFrame )
# bbox_ = get_rectangle( firstFrame )

# # setup initial location of window
# (x0, y0), (x1, y1) = bbox_
# print x0, x1, y0, y1
# c,w,r,h = x0, abs(x1-x0), y0, abs(y1 - y0)
# track_window = (c,r,w,h)
# print('Track window: %s' % str(track_window))


# # set up the ROI for tracking
# roi = firstFrame[r:r+h, c:c+w]
# hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
# roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
# cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
# term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

# while(1):
    # frame = vid.get_data( numFrame )
    # numFrame += 1
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

    # # apply meanshift to get the new location
    # ret, track_window = cv2.CamShift(dst, track_window, term_crit)
    # print track_window

    # ### Draw it on image
    # x,y,w,h = track_window
    # img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
    # # Draw it on image
    # ##pts = cv2.boxPoints(ret)
    # ##pts = np.int0(pts)
    # ##img2 = cv2.polylines(frame,[pts],True, 255,2)
    # cv2.imshow('img2',img2)
    # k = cv2.waitKey(60) & 0xff
    # if k == 27:
        # break
    # else:
        # cv2.imwrite(chr(k)+".jpg",img2)


# cv2.destroyAllWindows()
# cap.release()

# cap = cv2.VideoCapture( sys.argv[1] )

fgbg = cv2.createBackgroundSubtractorMOG2()

def get_mouse( cnts ):
    # Among all contours reject which are not mouse.
    possibleMouse = []
    for c in cnts:
        a = cv2.contourArea( c )
        if a > 50 and a < 500:
            possibleMouse.append( c )
        else:
            pass
    return possibleMouse

def get_trace( img ):
    cnts = cnt.contours( img, threshold_low = 100, threshold_high = 200 )
    mouseCnt = get_mouse( cnts )
    cntImg = np.zeros( img.shape )
    cv2.drawContours( cntImg, mouseCnt, -1, 255)
    return cntImg

while(1):
    frame = vid.get_data( numFrame )
    numFrame += 1
    fgmask = fgbg.apply(frame)
    mouseCntPlusNoise = get_trace( fgmask )
    newImg = 0.2 * cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) + mouseCntPlusNoise
    cv2.imshow('frame', newImg )
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
