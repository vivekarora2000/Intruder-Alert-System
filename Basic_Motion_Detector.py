import cv2 as cv
import numpy as np

    
cap = cv.VideoCapture(0)


if cap.isOpened():
    ret, frame = cap.read()
else:
    ret = False

ret, frame1 = cap.read()
ret, frame2 = cap.read()


while ret:
    

    d = cv.absdiff(frame1, frame2)
    
    grey = cv.cvtColor(d, cv.COLOR_BGR2GRAY)
    
    blur = cv.GaussianBlur(grey, (5, 5), 0)
    
    ret, th = cv.threshold( blur, 20, 255, cv.THRESH_BINARY)

    dilated = cv.dilate(th, np.ones((3, 3), np.uint8), iterations=1 )
    
    eroded = cv.erode(dilated, np.ones((3, 3), np.uint8), iterations=1 )
    
    img, c, h = cv.findContours(eroded, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    
    cv.drawContours(frame1, c, -1, (0, 255, 0), 2)
    

    cv.imshow("Output", frame1)
    if cv.waitKey(1) == 27: 
        break
    
    frame1 = frame2
    ret, frame2 = cap.read()

cv.destroyAllWindows()
cap.release()

