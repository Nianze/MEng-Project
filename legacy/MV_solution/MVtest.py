# Import everything needed to edit video clips
from moviepy.editor import *

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip("test_K5.AVI").subclip(50,60)

# Reduce the audio volume (volume x 0.8)
#clip = clip.volumex(0.8)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("TEST text",fontsize=70,color='white')

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_pos('center').set_duration(10)

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Generate an image clip
#im_clip = clip.to_ImageClip(t='00:01:00')# frame at t = 1 minute

# Write the result to a file (many options available !)
#video.write_videofile("TEST_edited.mp4")
clip.save_frame("frame.png", t='00:01:00')

# show the frame of clip at t = 10.5s, click somewhere to print 
# position and color of the pixel. press ESC to exit
clip.show(10.5, interactive=True)
my_clip.preview(fps=15, audio=False)