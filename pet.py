import sys
from pathlib import Path
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from random import randint


def resource_path(relative):
    # In der .exe liegt alles unter sys._MEIPASS, sonst neben dem Skript
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return str(base / relative)


FRAME_W = 16
FRAME_H = 16
FRAME_COUNT = 6
FRAME_MS = 100
SCALE = randint(3, 5)

MOVE_MS = 16
MOVE_SPEED = 1
LEFT = -1
RIGHT = 1

WALK = "walk"
LOOK = "look"
LOOK_LOOP = 3

SPRITE_LEFT = resource_path('src/slime blue left.png')
SPRITE_RIGHT = resource_path('src/slime blue right.png')
SPRITE_LOOKING = resource_path('src/slime blue looking.png')

class Sprite:
    
    def __init__(self, min_x, max_x):

        # Richtungen laden
        self.frames_left = self.load_frames(SPRITE_LEFT)
        self.frames_right = self.load_frames(SPRITE_RIGHT)
        self.frames_looking = self.load_frames(SPRITE_LOOKING, 10)
        self.frames_looking_right = self.frames_looking[5:] + self.frames_looking[:5]

        self.width = FRAME_W * SCALE
        self.height = FRAME_H * SCALE

        self.min_x = min_x
        self.max_x = max_x - self.width
        self.pos_x = self.min_x

        self.direction = RIGHT
        self.frames = self.frames_right
        self.frame_index = 0

        self.state = WALK
        self.loops_left = 0


    def contains(self, x, y):
        # Punkt im Fenster auf Sprite?
        return (self.pos_x <= x < self.pos_x + self.width
        and 0 <= y < self.height)


    def look(self):
        if self.state == LOOK:
            return
        self.state = LOOK
        if self.direction == RIGHT:
            self.frames = self.frames_looking_right
        else:
            self.frames = self.frames_looking
        self.frame_index = 0
        self.loops_left = LOOK_LOOP


    def load_frames(self, path, count=FRAME_COUNT):
        sheet = QPixmap(path)

        if sheet.isNull():
            print(f"Spritesheet not found: {path}")
            sys.exit(1)

        frames = []

        for x in range(count):
            frame = sheet.copy(x * FRAME_W, 0, FRAME_W, FRAME_H)
            frame = frame.scaled(
                FRAME_W * SCALE,
                FRAME_H * SCALE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
            frames.append(frame)
        return frames


    def current_frame(self):
        return self.frames[self.frame_index]


    def next_frame(self):
        # self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            if self.state == LOOK:
                self.loops_left -= 1
                if self.loops_left <= 0:
                    self.state = WALK
                    if self.direction == RIGHT:
                        self.frames = self.frames_right
                    else:
                        self.frames = self.frames_left


    def step(self):
        if self.state != WALK:
            return

        self.pos_x += MOVE_SPEED * self.direction

        if self.pos_x <= self.min_x:
            self.pos_x = self.min_x
            self.set_direction(RIGHT)
        elif self.pos_x >= self.max_x:
            self.pos_x = self.max_x
            self.set_direction(LEFT)


    def set_direction(self, direction):
        self.direction = direction
        if direction == RIGHT:
            self.frames = self.frames_right
        else:
            self.frames = self.frames_left