import os
import cv2
import glob
import sys
import numpy as np

# Get user supplied values
#imagePath = sys.argv[1]
#methodPath = sys.argv[2]

delimeter = '__'
format_fill = 4  # leading zeroes in sequence number

def feature_write(file, frame, result):
    if not os.path.exists(file):
        f = open(file,'w')
        f.write(frame.ljust(10) + result + '\n')
        f.close()
    else:
        f = open(file,'a')
        f.write(frame.ljust(10) + result + '\n')
        f.close()

def trav_file(cur_dir, targe_files):
    return glob.glob(cur_dir + targe_files)

def get_box_seq(box_dir):
    return box_dir[-format_fill:] # length of 'box' is 3

def get_frame_seq(frame_dir):
    return frame_dir[-format_fill-4:-4]

def get_frame_name(frame_dir):
    pic_name = frame_dir.split(delimeter)[1]
    return pic_name[:-format_fill-4]

def analysis_box(box): #read all the frames in the box_i
    frames = trav_file(box, '/*.png')
    for frame in frames:
        n = get_frame_seq(frame)
        name = get_frame_name(frame)
        img = cv2.imread(frame,0)
        hist,bins = np.histogram(img.ravel(),256,[0,256])
        hist.flatten().tolist()
        result = ''
        for item in hist:
        	result += str(item) + ' '
        if not os.path.exists('./bbox_features'):
            os.makedirs('./bbox_features')
        path = './bbox_features/' + name 
        if not os.path.exists(path):
            os.makedirs(path)
        feature_write(path+'/histogram'+'.dat', 
                      "frame" + str(n).zfill(format_fill), 
                      result)

if not os.path.exists('./bboxes'):
    print "no frames source file detected!"
else:
    cur_dir = os.getcwd()
    box_dir = trav_file(cur_dir, '/bboxes/*')
    for box in box_dir:
        analysis_box(box)
    print 'Analysis done !'