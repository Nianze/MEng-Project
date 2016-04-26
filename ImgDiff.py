import os
import cv2
import glob
import sys
from skimage.measure import compare_ssim as ssim

# Get user supplied values
#imagePath = sys.argv[1]
#methodPath = sys.argv[2]

delimeter = '__'
format_fill = 4  # leading zeroes in sequence number
global buff # buffer of previous img

def feature_write(file, frame, result):
    if not os.path.exists(file):
        f = open(file,'w')
        f.write(frame.ljust(10) + result.rjust(5) + '\n')
        f.close()
    else:
        f = open(file,'a')
        f.write(frame.ljust(10) + result.rjust(5) + '\n')
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
    global buff
    for frame in frames:
        n = get_frame_seq(frame)
        if n == '0000':
        	buff = frame
        	continue
        name = get_frame_name(frame)
        prev = cv2.imread(buff)
        prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        curr = cv2.imread(frame)
        curr = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
        result = ssim(prev,curr)
        if not os.path.exists('./bbox_features'):
            os.makedirs('./bbox_features')
        path = './bbox_features/' + name 
        if not os.path.exists(path):
            os.makedirs(path)
        feature_write(path+'/img_diff'+'.dat', 
                      "frame" + str(n).zfill(format_fill), 
                      str(result))
        buff = frame # update the buffer to current frame before next loop

if not os.path.exists('./bboxes'):
    print "no frames source file detected!"
else:
    cur_dir = os.getcwd()
    box_dir = trav_file(cur_dir, '/bboxes/*')
    for box in box_dir:
        analysis_box(box)
    print 'Analysis done !'