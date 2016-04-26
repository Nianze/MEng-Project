import cv2
import numpy as np 
import os
#import errno
import json

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
cap = cv2.VideoCapture('test.mp4')
font = cv2.FONT_HERSHEY_SIMPLEX
drawing = True # if mouse is pressed, do not draw the box

init_x,init_y = -1,-1 # temp buffer to store init x,y position of mouse
mouse_pos = [] # store the mouse position

to_save = False # a flag to indicate whether to save the image
f_lapse = 30 # indicate number of frames between two output img to be saved
f_count = 0  # work with f_lapse to ignore frames within every f_lapse ones
n_frame = 0 # count the number of extracted image
to_show = True # indicate whether or not to show the image

# mouse callback function
def draw(event,x,y,flags,param):
    global init_x,init_y #,drawing
    if event == cv2.EVENT_LBUTTONDOWN:
#        drawing = True
        init_x, init_y = x,y
    elif event == cv2.EVENT_LBUTTONUP:
#        drawing = True
        mouse_pos.append({'ix':init_x,'iy':init_y,'ex':x,'ey':y})

# bind the function to window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

# extract every selected binding box
def extract(boxes,n):
    if not os.path.exists('./bboxes'):
        os.makedirs('./bboxes')
    for i,box in enumerate(boxes):
        path = './bboxes/box'+str(i)
        if not os.path.exists(path):
            os.makedirs(path)
        out_img = cv2.resize(box,(100,100))
        cv2.imwrite(path+'/frame'+str(n)+'.png', out_img)

while (cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        #scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Draw a rectangle around the target area selected by mouse   

#   get the binding boxes' coordinates
    preview = []
    for i,pos in enumerate(mouse_pos):
        ix = min(pos['ix'],pos['ex'])
        iy = min(pos['iy'],pos['ey'])
        ex = max(pos['ix'],pos['ex'])
        ey = max(pos['iy'],pos['ey'])
        l = max(ex-ix,ey-iy)
        preview.append(frame[iy:(iy+l),ix:(ix+l)]) #img[y: y + h, x: x + w] 

#   keyboard operation
    key = cv2.waitKey(10)
    if key == ord('f') or key == ord('F'):
        continue
    if key == 27 or key == ord('q'):
        break
    if key == ord(' '):
        if not os.path.exists('./preview'):
            os.makedirs('./preview')
        for i,box in enumerate(preview):
            out_img = cv2.resize(box,(100,100))
            cv2.imwrite('./preview/box'+str(i)+'.png', out_img)
    if key == ord('s'):
        to_save = True
    if key == ord('S'):
        to_save = False
    if key == ord('d'):
        # delete the binding boxes in reverse order
        if len(mouse_pos) > 0:
            del mouse_pos[-1]
    if key == ord('D'):
        # delete all the binding boxes
        mouse_pos = []
    if key == ord('w'):
    	# stop showing the image
        to_show = False
    if key == ord('W'):
    	# showing the image
        to_show = True
    if key == ord('c'):
    	# save the current configuration to the file config
    	f = open('config','w')
    	json.dump(mouse_pos,f)
    	f.close()
    if key == ord('C'):
    	# load the current configuration from the file config
    	if os.path.exists('config'):
    		f = open('config','r')
    		mouse_pos = json.load(f)
    		f.close()

#   extract all the binding box frames
    if to_save:
        f_count += 1
        if f_count >= f_lapse:
            extract(preview,n_frame)
            n_frame += 1
            f_count = 0

#   show the image        
    if to_show:  
        for i,pos in enumerate(mouse_pos):
            ix = min(pos['ix'],pos['ex'])
            iy = min(pos['iy'],pos['ey'])
            ex = max(pos['ix'],pos['ex'])
            ey = max(pos['iy'],pos['ey'])
            l = max(ex-ix,ey-iy)
            cv2.rectangle(frame, (ix,iy),(ix+l,iy+l),(0,255,0),1)       
            cv2.putText(frame,'Binding Box ' + str(i),(ix,iy+l),font,0.5,(0,0,255),1,cv2.CV_AA)
    if to_show :
        cv2.putText(frame,'space: preview; d/D: delete binding boxes; '+
                's/S: start/stop to extract bboexs; f: speed up fps; '+ 
                'w: turn off the image; W:turn on the image' + 
                'c: save the config file; C: read the config file',
                (0,int(cap.get(4))-5),font,0.5,(0,255,255),1,cv2.CV_AA)
        cv2.imshow('image',frame)

# when finished, release the capture
cap.release()
cv2.destroyAllWindows()
