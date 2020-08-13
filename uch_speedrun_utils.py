import json
import keyboard
import pywinauto
import time

from keyboard._keyboard_event import KeyboardEvent

# Scan code mapping for keys.
JUMP = 57 # Spacebar
SPRINT = 42 # Shift
# SPRINT = 39 # Semicolon
UP = 17 # w
LEFT = 30 # a
DOWN = 32 # s
RIGHT = 31 # d
RETRY = 48 # b

NAMES = {
  57: "space",
  39: ";",
  42: "shift",
  17: "w",
  30: "a",
  32: "s",
  31: "d",
  48: "b"
}

# Key press types
KEY_DOWN = "down"
KEY_UP = "up"

class Speedrun:

  def __init__(self, fps=60, width=0.5, slices=3):
    self.fps = fps
    self.per_frame = 1 / fps
    self.width_adjust = [i * self.per_frame * width / slices for i in range(slices + 1)]
    self.frame = 0
    self.events = []
    return

  def increment_frames(self, increment=0):
    """Kinda unnecessary but makes sense as an api."""
    self.frame += increment

  def press(self, code, time=None):
    for adjust in self.width_adjust:
      self.events.append(KeyboardEvent(KEY_DOWN, code, name=NAMES[code], time=(time or self.frame * self.per_frame) + adjust))

  def release(self, code, time=None):
    for adjust in self.width_adjust:
      self.events.append(KeyboardEvent(KEY_UP, code, name=NAMES[code], time=(time or self.frame * self.per_frame) + adjust))

  def press_and_release(self, code, duration=0):
    """Creates a 'held key' event.

    This creates both a key down and key up event with the key up event occuring
    the specified duration after the key down event occurs.
    """
    self.press(code)
    end_time = (self.frame + duration) * self.per_frame
    if duration == 0:
      end_time += 0.0001
    self.release(code, time=end_time)

  def save(self, f):
    """Saves the run to json."""
    self.events = sorted(self.events, key=lambda event: event.time)
    with open(f, "w") as wh:
      json.dump([json.loads(event.to_json()) for event in self.events], wh, indent=2)

  def load(self, f):
    """Loads a run from json."""
    with open(f, "r") as rh:
      self.events = json.load(rh)

  def play(self, speed=1.0):
    """Playback our recorded events.

    There's a play() method on the keyboard class that does literally what this
    function does. Except for some reason it doesn't work with manual events.
    """
    # Focus on the UCH window first.
    app = pywinauto.application.Application().connect(best_match="Ultimate Chicken Horse")
    window_ids = pywinauto.findwindows.find_windows(title="Ultimate Chicken Horse")
    window = app.window(handle=window_ids[0])
    window.set_focus()
    # Wait a bit then go.
    time.sleep(1)

    last_time = None
    self.events = sorted(self.events, key=lambda event: event.time)
    for event in self.events:
      if last_time is not None:
        time.sleep((event.time - last_time) / speed)
      last_time = event.time
      keyboard.press(event.name) if event.event_type == KEY_DOWN else keyboard.release(event.name)
