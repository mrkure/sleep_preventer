# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:08:29 2022

@author: CAZ2BJ
"""
from mklib.lib_io import mkIO
mkIO.activate_env(1, "base",__file__,0)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import  QSystemTrayIcon, QWidget, QAction, QMenu, QApplication

import threading, os, sys
import win32api, win32con, time

path_icon_running = rf'{os.path.dirname(os.path.realpath(__file__))}\res\running.png'
path_icon_stopped = rf'{os.path.dirname(os.path.realpath(__file__))}\res\stopped.png'

class SleepPreventer(QSystemTrayIcon):
    def __init__(self, parent):
        QSystemTrayIcon.__init__(self, QIcon(path_icon_running), parent)
        
        self.icon_running   = QIcon(path_icon_running)           
        self.icon_stopped   = QIcon(path_icon_stopped)  
        
        menu = QMenu(parent)
        self.setContextMenu(menu)
        
        # close option
        option_close = QAction("Close")
        menu.addAction(option_close)
        option_close.triggered.connect(self.on_close)        


        # on any click at icon 
        self.activated.connect(self.on_systray_activated)
        
        # thread
        self.running = True        
        self.thread1 = threading.Thread( target=self.move, args = ())
        self.thread1.setDaemon(True)
        self.thread1.start()
        
        menu = QMenu(parent)
        self.setContextMenu(menu)
        
        exitAction = menu.addAction("Close")
        exitAction.triggered.connect(self.on_close)
        
        self.show()

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
            if time%60 == 0 and self.running:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)

#%% MAIN        
if __name__ == '__main__':
    app    = QApplication(sys.argv)
    widget = QWidget()
    sleep_preventer = SleepPreventer(widget)
    sys.exit(app.exec_())
    
