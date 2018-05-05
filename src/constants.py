CFG_MPV = """#########
# Video #
#########

# HQ preset, uses Spline36 for upscaling and Mitchell-Netravali for downscaling
# Debanding is disabled beacause we don't want to alter the video while doing quality control
vo=opengl-hq
profile=gpu-hq
deband=no

# Potentially higher quality video output
# Might be too demanding for old or low end hardware
#scale=ewa_lanczossharp
#cscale=ewa_lanczossoft
#dscale=lanczos


#############
# Subtitles #
#############

# This disables the removal of very small gaps between subtitle lines
# This might be a nice feature, but it hides flaws in the script
# We don't want that while doing quality control
sub-fix-timing=no

# This makes sure that the current subtitle line is loaded after seeking
demuxer-mkv-subtitle-preroll=yes


###########
# OSC/OSD #
###########

# Very slim On Screen Controller that consists of only a seekbar
# Change the value of osc-valign to set the vertical position (Values between -1 and 1 are allowed)
script-opts=osc-minmousemove=0,osc-hidetimeout=200,osc-layout=slimbox,osc-valign=0.6
osd-bar-align-y=0

# Bigger On Screen Controller with many buttons
#script-opts=osc-minmousemove=0,osc-hidetimeout=200,osc-layout=box,osc-valign=0.5


###############
# Screenshots #
###############

screenshot-format=png
screenshot-high-bit-depth=no
screenshot-directory=~~/Screenshots/
"""

CFG_INPUT = """############################################
# The following keys are reserved by mpvQC #
# Changing them here will have no effect   #
############################################

e ignore
f ignore
UP ignore
DOWN ignore
ctrl+s ignore
ctrl+S ignore
ctrl+n ignore
ctrl+o ignore
ctrl+q ignore
ctrl+O ignore
ctrl+alt+O ignore
ctrl+r ignore
MOUSE_BTN2 ignore    # Right mouse click

##################################################
# The following keys can be bound to anything    #
# This is not a comprehensive list of all keys   #
# There are many more, like a, A, @, ö, é, î ... #
# Please never bind 'quit' to any key!           #
##################################################

SPACE cycle pause
LEFT no-osd seek -2 relative+exact
RIGHT no-osd seek 2 relative+exact
shift+LEFT osd-bar seek -5 relative+keyframes
shift+RIGHT osd-bar seek 5 relative+keyframes
ctrl+LEFT no-osd sub-seek -1
ctrl+RIGHT no-osd sub-seek 1

MOUSE_BTN0 cycle pause       # Left click on mouse
MOUSE_BTN3 add volume 2      # Mouse wheel up
MOUSE_BTN4 add volume -2     # Mouse wheel down
MOUSE_BTN5 add chapter -1    # Backward button on mouse
MOUSE_BTN6 add chapter 1     # Forward button on mouse

p cycle pause
. frame-step
, frame-back-step
9 add volume -2
0 add volume 2
m cycle mute
j cycle sub
J cycle sub down
SHARP cycle audio        # SHARP assigns the # key
l ab_loop
s screenshot subtitles
S screenshot window

# This burns in subtitles (i.e. always render them at video resolution)
# It cycles through the values "no" (Don't blend subtitles with the video)
#                              "yes" (Blend at display resolution)
#                              "video" (Blend at video resolution)
b cycle blend-subtitles

# This displays statistics of the currently played file
i script-binding stats/display-stats-toggle
"""

CREDITS = """<h1 style='text-align:center;'>{} - {}</h1>
<p>
    <b>{}</b> is a free, open source and <b>libmpv</b> based application for
    the quick and easy creation of quality control reports of video files.
</p>
<p>Based on {} and ffmpeg {}</p>
<p>
    Copyright © {} Frechdachs<br>&lt;frechdachs@rekt.cc&gt;
</p>
<p>
    <a href='https://mpvqc.rekt.cc/'>https://mpvqc.rekt.cc/</a>
</p>"""
