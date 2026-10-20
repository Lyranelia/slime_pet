import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
import pet


WINDOW_HEIGHT = pet.FRAME_H * pet.SCALE

class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slimey Desktop Pet!")

        # Transparenz und so
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.usable_rect = QApplication.primaryScreen().availableGeometry()
        self.pos_y = self.usable_rect.y() + self.usable_rect.height() - WINDOW_HEIGHT + (2 * pet.SCALE)

        # setGeometry(x, y, width, height)
        self.setGeometry(self.usable_rect.x(), self.pos_y, self.usable_rect.width(), WINDOW_HEIGHT)

        self.sprite = pet.Sprite(0, self.usable_rect.width())

        # Timer Setup Animation
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.on_anim)
        self.anim_timer.start(pet.FRAME_MS)

        # Timer Setup Movement
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.on_move)
        self.move_timer.start(pet.MOVE_MS)

    def on_anim(self):
        self.sprite.next_frame()
        self.update()

    def on_move(self):
        self.sprite.step()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.sprite.pos_x, 0, self.sprite.current_frame())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            if self.sprite.contains(pos.x(), pos.y()):
                self.sprite.look()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PetWindow()
    window.show()
    
    sys.exit(app.exec())