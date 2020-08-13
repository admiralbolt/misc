"""
A speedrun of chameleon cage 2 3V0S-XR71

All the keyboard events are programmed out and played back.
Creating this is going to suck.
"""
import sys
import time

from uch_speedrun_utils import *

FPS = 120
run = Speedrun(fps=FPS, width=0.95)

# Start the run
run.press_and_release(JUMP, duration=0)

run.press(SPRINT)
run.press(RIGHT)

##############
# FLOOR 1 #
###############

# First jump onto gray blocks.
run.increment_frames(30)
run.press_and_release(JUMP, duration=10)

run.increment_frames(45)

# Jump onto second set of gray blocks
# Hold space to get a quick drop the ez way.
run.press(JUMP)

# Wait until after we fall, then let go of JUMP
run.increment_frames(190)
run.release(JUMP)
run.increment_frames(16)
run.press_and_release(JUMP, duration=50)

# Wait until just before we land, start holding jump to buffer it
run.increment_frames(50)
run.press(JUMP)

# Buffer a jump off the right wall
# it also needs to be a quick jump.
run.increment_frames(48)
run.release(JUMP)
run.increment_frames(4)
run.release(RIGHT)
run.release(SPRINT)
run.press(LEFT)
run.press(JUMP)
run.increment_frames(12)
run.press(SPRINT)

# Slide to max height on left wall, then quick jump.
run.increment_frames(32)
run.release(JUMP)
run.increment_frames(4)
run.release(SPRINT)
run.press(JUMP)
run.increment_frames(12)
run.press(SPRINT)
run.increment_frames(44)
run.release(JUMP)


###########
# FLOOR 2 #
###########

# Land, run for a bit then full jump
run.increment_frames(22)
run.press_and_release(JUMP, 50)

# Run, the full jump precisely to setup a corner jump.
run.increment_frames(117)
run.press_and_release(JUMP, 60)

run.increment_frames(61)
run.press(JUMP)
run.increment_frames(70)
run.release(JUMP)
run.increment_frames(19)
run.release(LEFT)
run.press(RIGHT)

# Slide off, big jump
run.increment_frames(19)
run.press_and_release(JUMP, 50)
run.increment_frames(80)
run.release(SPRINT)
run.increment_frames(4)
run.press_and_release(JUMP, 24)
run.increment_frames(4)
run.press(SPRINT)
run.increment_frames(24)

# land, then wide jump
run.increment_frames(47)
run.press_and_release(JUMP, 40)
run.increment_frames(1)
run.release(RIGHT)
run.increment_frames(1)
run.press(LEFT)

# Land, then jump
run.increment_frames(51)
run.release(LEFT)
run.press(RIGHT)
run.increment_frames(22)
run.press_and_release(JUMP, 40)
run.increment_frames(2)
run.release(RIGHT)
run.press(LEFT)

# DO IT
run.increment_frames(40)
run.release(LEFT)
run.press(RIGHT)
run.press_and_release(JUMP, 50)

# BONK
run.increment_frames(80)
run.press(JUMP)

# Clear everything
run.increment_frames(FPS)
run.release(SPRINT)
run.release(RIGHT)
run.release(LEFT)
run.release(UP)
run.release(DOWN)
run.release(JUMP)
# run.press_and_release(RETRY, 100)

run.play(speed=1)
run.save("chameleon_cage_2.json")
