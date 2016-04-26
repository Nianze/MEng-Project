import pygame as py
from moviepy.editor import *
#import gizeh

def make_frame(t):
    #surface = gizeh.Surface(1280,720) # width, height
    #radius = W*(1+ (t*(2-t))**2 )/6 # the radius varies over time
    #circle = gizeh.circle(radius, xy = (64,64), fill=(0,1,0))
    #circle.draw(surface)
    return surface.get_npimage() # returns a 8-bit RGB array

drawing = False # true if mouse is pressed
ix,iy = -1,-1
ex,ey = -1,-1

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip("test_K5.AVI")#.subclip(50,60)

#screen = pg.display.set_mode(clip.size) 
#def gatherClicks(t):
#	global ix,iy,ex,ey,drawing
#    #imdisplay(clip.get_frame(t),screen)
#    while (1):
#        for event in pg.event.get():
#            if event.type == pg.KEYDOWN:
#                if (event.key == pg.K_BACKSLASH):
#                    return "return"
#            elif event.type == pg.MOUSEBUTTONDOWN:
#                x, y = pg.mouse.get_pos()
#                drawing = False
#                ix,iy = x,y
#            elif event.type == pg.MOUSEBUTTONUP:
#            	x, y = pg.mouse.get_pos()
#            	drawing = True
#                ex,ey = x,y

#maskclip = VideoClip(make_frame, duration=2, ismask=True) # 2 seconds
maskclip = ImageClip("doge.jpg", ismask=True)
clip.set_mask(maskclip)
clip.save_frame("frame.png", t='00:00:05')
clip.preview(fps=25, audio=False)