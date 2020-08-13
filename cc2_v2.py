"""
Attempt #2 at chameleon cage 2
"""

import sys
import time

from uch_speedrun_utils import *

FPS = 60
run = Speedrun(fps=FPS, width=0.95, slices=10)

# Buffer held jump sprint and right
run.press(JUMP)
run.press(RIGHT)
run.press(SPRINT)
run.increment_frames(25)
run.release(JUMP)

# Jump out of the bottom
run.increment_frames(41)
run.press_and_release(JUMP, 30)

# Land, run, jump onto first climb
run.increment_frames(67)
run.press_and_release(JUMP, 21)

# Buffer an instant jump
run.increment_frames(26)
run.release(RIGHT)
run.increment_frames(5)
run.press(JUMP)
run.increment_frames(9)
run.press(RIGHT)

# Jump from right wall to left wall
run.increment_frames(22)
run.release(JUMP)
run.release(RIGHT)
run.release(SPRINT)
run.increment_frames(1)
run.press(JUMP)
run.increment_frames(1)
run.press(SPRINT)

# Quick jump after sliding
run.increment_frames(18)
run.release(JUMP)
run.release(SPRINT)
run.press(LEFT)
run.increment_frames(1)
run.press_and_release(JUMP, 19)
run.increment_frames(1)
run.press(SPRINT)

# LEVEL 2
# Run, then full jump
run.increment_frames(37)
run.press_and_release(JUMP, 25)

# Run, the full jump precisely to setup a corner jump.
run.increment_frames(53.5)
run.press_and_release(JUMP, 30)

# Corner jump
run.increment_frames(40)
run.press(JUMP)
# Slide up the wall, land on the top post
run.increment_frames(21)
run.release(JUMP)
run.increment_frames(14)
run.release(LEFT)
run.increment_frames(1)
run.press(RIGHT)

# Slide off, jump
run.increment_frames(11)
run.press_and_release(JUMP, 30)

# Buffered quick jump on platform
run.increment_frames(40)
run.release(SPRINT)
run.increment_frames(1)
run.press_and_release(JUMP, 9)
run.increment_frames(1)
run.press(SPRINT)

# Land, run, wide jump
run.increment_frames(33)
run.press_and_release(JUMP, 19)
run.increment_frames(1)
run.release(RIGHT)
run.press(LEFT)

# Drift right just before we land
run.increment_frames(22)
run.release(LEFT)
run.press(RIGHT)

# Jump again
run.increment_frames(8)
run.press_and_release(JUMP, 25)
run.increment_frames(2)
run.release(RIGHT)
run.press(LEFT)

# DO IT
run.increment_frames(25)
run.press(JUMP)
run.release(LEFT)
run.press(RIGHT)


# CLeanup
run.increment_frames(FPS * 2)
run.release(SPRINT)
run.release(RIGHT)
run.release(LEFT)
run.release(UP)
run.release(DOWN)
run.release(JUMP)
run.press_and_release(RIGHT, 1)
run.press_and_release(RETRY, 80)

run.play()
