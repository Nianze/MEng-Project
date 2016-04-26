import cv2
import numpy as np 
import os
import sys

start_sec = sys.argv[1]

cap = cv2.VideoCapture('test.mp4')
dict = {} #key = student name, value = [x1,y1,x2,y2], where (x1,y1) is leftup point, (x2,y2) is rightdown point

n_frame = 0 # count the number of extracted image
cur_time = float(start_sec) # current time in seconds
time_lapse = 1 # time lapse interval in second
format_fill = 4  # leading zeroes in sequence number
delimeter = '__'


# extract every selected binding box
# frames: [['Alice',subframe1],['Bob',subframe2],...]
# n: nth frame
def extract(frames,n):
    if not os.path.exists('./bboxes'):
        os.makedirs('./bboxes')
    for i,name_frame in enumerate(frames):
        path = './bboxes/box'+str(i).zfill(format_fill) 
        if not os.path.exists(path):
            os.makedirs(path)
        name = delimeter+name_frame[0]#.rjust(10,' ')
        subFrame = name_frame[1]

        out_img = cv2.resize(subFrame,(100,100))
        cv2.imwrite(path+'/'+name+str(n).zfill(format_fill)+'.png', out_img)

# read config file and get the boundting box coordinary
if os.path.exists('coordinates.txt'):
    lines = [line.rstrip('\n') for line in open('coordinates.txt')]
    for line in lines:
        name = line.split()[4]
        mouse_pos = map(int, line.split()[0:4])
        dict[name] = mouse_pos
    try:
        cap.set(0, cur_time*1000)  # cue to start sec. position. cv2.CV_CAP_PROP_POS_MSEC=0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if frame is None:
                break
            print 'current time: ' + str(cur_time)
            #extract all the binding box frames
            subFrames = []
            for key,pos in dict.iteritems():
                ix = min(pos[0],pos[1])
                ex = max(pos[0],pos[1])
                iy = min(pos[2],pos[3])
                ey = max(pos[2],pos[3])
                l = max(ex-ix,ey-iy)
                #subFrames.append([key,frame[pos[1]:(pos[1]+l),pos[0]:(pos[0]+l)]])
                subFrames.append([key,frame[iy:(iy+l),ix:(ix+l)]])
            extract(subFrames,n_frame)
            n_frame += 1
            cur_time += time_lapse
            cap.set(0, cur_time*1000)
        # when finished, release the capture
        print 'Extraction over.'
        cap.release()
    except KeyboardInterrupt:
        print '\nExtraction interrupted.'
else:
    print "No coordinates.txt file found :("
