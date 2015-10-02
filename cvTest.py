import cv2
import numpy as np 

cap = cv2.VideoCapture('test_k5.AVI')
font = cv2.FONT_HERSHEY_SIMPLEX
drawing = False # true if mouse is pressed
ix,iy = -1,-1
ex,ey = -1,-1

# mouse callback function
def draw(event,x,y,flags,param):
    global ix,iy,ex,ey,drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = False
        ix,iy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = True
        ex,ey = x,y
# bind the function to window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

while (cap.isOpened()):
    ret, frame = cap.read()
    if drawing == True:
    	cv2.rectangle(frame, (ix,iy),(ex,ey),(0,255,0),2)
        cv2.putText(frame, '  Target confirmed!',(ix,(ey+iy)//2),font,0.5,(0,0,255),1,cv2.CV_AA)
        crop_im = frame[iy:ey,ix:ex] #img[y: y + h, x: x + w] 
    cv2.imshow('image',frame)
    key = cv2.waitKey(10)
    if key == 27:
      break
    if key == ord(' '):
      cv2.imwrite('croped image.jpg', crop_im)
# when finished
cap.release()
cv2.destroyAllWindows()