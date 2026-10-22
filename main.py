import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QMenu
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
import pet


WINDOW_HEIGHT = pet.FRAME_H * pet.SCALE


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slimey Desktop Pet!")

        

        # Menu Creation
        self.menu = QMenu(self)
        title = self.menu.addAction("Slime Menu")
        title.setEnabled(False)

        colorChange = self.menu.addMenu("change color")
        sizeChange = self.menu.addMenu("change size")
        separator = self.menu.addSeparator()
        exitAction = self.menu.addAction("exit")

        self.menu.setStyleSheet(Path(pet.resource_path("src/style.css")).read_text(encoding="utf-8"))

        self.menu.setWindowFlags(self.menu.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Menu Connection
        colorChange.triggered.connect(self.colorChange_triggered)
        sizeChange.triggered.connect(self.sizeChange_triggered)
        exitAction.triggered.connect(QApplication.quit)

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


    # +++++++++++++++++++++++++++++++++++ HIER CONTEXT MENU +++++++++++++++++++++++++++++++++++
    def contextMenuEvent(self, event):
        self.sprite.hold()
        self.menu.exec(event.globalPos())
        self.sprite.release()
        # in Sprite Klasse abfangen, da dann das Menu vom Fenster öffnen
        # Menu auch Instanz vom aktuellen Slime übergeben
        # sodass ich dann entweder eine Fensteraktion machen kann (weiteren Slime hinzufügen) oder
        # am Sprite was machen, wie Farbe ändern oder Größe

    def colorChange_triggered(self):
        print("Color change!")
        # Was könnwer denn machen:
        # exit-Button, der's wichtig
        # - das wär dann eher der letzte Button
        # - cool, hab ich
        # Bereich, in dem ich eine spezifische Farbe auswählen kann, out of meinen 5
        # - 5 entsprechend farbige Kästchen, die Farbe kann ich ja libreSprite entnehmen im Hexcode oder so
        # Bereich, in dem ich eine Größe angeben kann, also SCALE 3-5 (smol, medium, big)
        # - Slider dafür?
    def sizeChange_triggered(self):
        print("Size change!")

    # +++++++++++++++++++++++++++++++++++++++++ ENDE +++++++++++++++++++++++++++++++++++++++++


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