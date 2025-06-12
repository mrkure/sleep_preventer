"""sleep preventer"""

import os
import time
import threading
import win32api
import win32con

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QSystemTrayIcon, QWidget, QAction, QMenu, QApplication

PATH_ICON_RUNNING = rf"{os.path.dirname(os.path.realpath(__file__))}\res\running.ico"
PATH_ICON_STOPPED = rf"{os.path.dirname(os.path.realpath(__file__))}\res\stopped.ico"


class SleepPreventer(QSystemTrayIcon, QWidget):
    """sleep preventer class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TRAY SETTINGS ------------------------------
        self.icon_running = QIcon(PATH_ICON_RUNNING)
        self.icon_stopped = QIcon(PATH_ICON_STOPPED)
        self.setIcon(self.icon_running)

        menu = QMenu()
        self.setContextMenu(menu)

        self.action_close = QAction("Close")
        menu.addAction(self.action_close)

        self.action_close.triggered.connect(self._on_close)
        self.activated.connect(self._on_systray_activated)

        # thread
        self.running = True
        self.thread1 = threading.Thread(target=self.move, args=(), daemon=True)
        self.thread1.start()

        self.running = True
        self.setVisible(True)
        self.show()

    # CALLBACKS ------------------------------
    def _on_close(self):
        self.hide()
        QCoreApplication.quit()

    def _on_systray_activated(self, i_reason):
        if i_reason == 3:
            self.switch_state()

    # METHODS ------------------------------
    def switch_state(self):
        """switch state between on and off"""
        if self.running:
            self.setIcon(self.icon_stopped)
            self.running = False

        elif not self.running:
            self.setIcon(self.icon_running)
            self.running = True

    def move(self):
        """move mouse by zero pixels each 10 seconds"""
        _time = 0
        while True:
            time.sleep(1)
            _time += 1
            if _time % 10 == 0 and self.running:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)


# MAIN ------------------------------
if __name__ == "__main__":
    app = QApplication([])
    sleep_preventer = SleepPreventer()
    app.exec()
