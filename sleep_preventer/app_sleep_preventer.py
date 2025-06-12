# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:08:29 2022

@author: CAZ2BJ
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import  QSystemTrayIcon, QWidget, QAction, QMenu, QApplication

import threading, os, sys
import win32api, win32con, time

path_icon_running = rf'{os.path.dirname(os.path.realpath(__file__))}\res\running.ico'
path_icon_stopped = rf'{os.path.dirname(os.path.realpath(__file__))}\res\stopped.ico'

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
        
        self.action_close.triggered.connect(self.on_close)   
        self.activated.connect(self.on_systray_activated)
        
        # thread
        self.running = True        
        self.thread1 = threading.Thread( target=self.move, args = (), daemon=True)
        self.thread1.start()
      
        self.running = True       
        self.setVisible(True)  
        self.show()
 
#%% METHODS
    def on_window_hide(self, string):
        self.window.hide()
        self.setIcon(self.icon_stopped)
        self.running = False
        

#%% CALLBACKS      
    def on_close(self):     
        self.hide()
        QCoreApplication.quit() 
        
    def on_systray_activated(self, i_reason):
        if i_reason == 3:
            self.switch_state()
                    
    def switch_state(self):  
        if self.running:
            self.setIcon(self.icon_stopped)  
            self.running = False
            
        elif not self.running:
            self.setIcon(self.icon_running)  
            self.running = True  
            
    def move(self):
        _time = 0
        while True:   
            time.sleep(1)
            _time += 1
            if _time%10 == 0 and self.running:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)

#%% MAIN  
if __name__ == "__main__":
    app = QApplication([])
    sleep_preventer = SleepPreventer()
    app.exec()