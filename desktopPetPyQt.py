import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer


def resource_path(relative):
    # In der .exe liegt alles unter sys._MEIPASS, sonst neben dem Skript
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return str(base / relative)


FRAME_W = 16
FRAME_H = 16
FRAME_COUNT = 6
FRAME_MS = 100
SCALE = 4

MOVE_MS = 16
MOVE_SPEED = 1
LEFT = -1
RIGHT = 1

SPRITE_LEFT = resource_path('src/slime blue left.png')
SPRITE_RIGHT = resource_path('src/slime blue right.png')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slimey Desktop Pet!")

        # Transparenz und so
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # Richtungen laden
        self.frames_left = self.load_frames(SPRITE_LEFT)
        self.frames_right = self.load_frames(SPRITE_RIGHT)

        # nach rechts moven
        self.direction = RIGHT
        self.frames = self.frames_right

        # erstes Bild anzeigen lassen in einem QLabel
        self.frame_index = 0
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.label.setPixmap(self.frames[0])
        self.resize(self.frames[0].size())

        

        # tatsächlich moven
        self.usable_rect = QApplication.primaryScreen().availableGeometry()
        self.min_x = self.usable_rect.x()
        self.max_x = self.usable_rect.x() + self.usable_rect.width() - self.width()
        self.pos_x = self.min_x
        self.pos_y = self.usable_rect.y() + self.usable_rect.height() - self.height()
        self.move(self.pos_x, self.pos_y)
        # bewegt gesamtes Fenster, mal was anderes ausprobieren
        # Fensterbreite anpassen auf usable_rect.width, dann move ersetzen
        # zeichnen neu aufrufen an neuer pos_x
        
        self.place_on_taskbar()

        # Timer Setup Animation
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.next_frame)
        self.anim_timer.start(FRAME_MS)

        # Timer Setup Movement
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_above_taskbar)
        self.move_timer.start(MOVE_MS)


    def load_frames(self, path):
        sheet = QPixmap(path)


        if sheet.isNull():
            print(f"Spritesheet not found: {path}")
            sys.exit(1)


        frames = []

        for x in range(FRAME_COUNT):
            frame = sheet.copy(x * FRAME_W, 0, FRAME_W, FRAME_H)
            frame = frame.scaled(
                FRAME_W * SCALE,
                FRAME_H * SCALE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
            frames.append(frame)
        return frames


    def next_frame(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.label.setPixmap(self.frames[self.frame_index])


    def place_on_taskbar(self):
        
        self.x = self.usable_rect.x() + self.usable_rect.width() - self.width()
        self.y = self.usable_rect.y() + self.usable_rect.height() - self.height() + (2 * SCALE)      # das mit SCALE wegen den 2 transparenten Pixeln aufm Spritesheet

        self.move(self.x, self.y)


    def move_above_taskbar(self):
        self.pos_x += MOVE_SPEED * self.direction

        if self.pos_x <= self.min_x:
            self.pos_x = self.min_x
            self.set_direction(RIGHT)
        elif self.pos_x >= self.max_x:
            self.pos_x = self.max_x
            self.set_direction(LEFT)
        
        self.move(self.pos_x, self.y)


    def set_direction(self, direction):
        self.direction = direction
        if direction == RIGHT:
            self.frames = self.frames_right
        else:
            self.frames = self.frames_left


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())