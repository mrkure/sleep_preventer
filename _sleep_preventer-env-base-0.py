# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:08:29 2022

@author: CAZ2BJ
"""
from mklib.lib_io import mkIO
mkIO.activate_env(1, __file__)

from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QSystemTrayIcon, QWidget, QAction

import win32api, win32con, time
import threading, os, sys

class SleepPreventer(QSystemTrayIcon, QWidget):
    def __init__(self):
        super(QSystemTrayIcon, self).__init__()
        super(QWidget, self).__init__()
        try:
            self.dirr = os.path.dirname(os.path.realpath(__file__))              
        except:            
            self.dirr = os.path.dirname(sys.executable)  

        self.icon_running   = QIcon('{}\{}'.format(self.dirr + '/resources', "running.png"))           
        self.icon_stopped   = QIcon('{}\{}'.format(self.dirr + '/resources', "stopped.png"))    
        self.setIcon(self.icon_running) 
        
        self.menu = QtWidgets.QMenu()       
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.setContextMenu(self.menu)  
        self.setVisible(True)  

        self.activated.connect(self.on_systray_activated)
        self.option_close.triggered.connect(self.on_close)       
       
        self.running = True        
        self.thread1 = threading.Thread( target=self.move, args = ( ))
        self.thread1.setDaemon(True)
        self.thread1.start()

      

    def on_systray_activated(self, i_reason):
        if i_reason == 3:
            self.switch_state()
            
    def on_close(self):     
        self.running = -1
        self.hide()
        self.close()   
        
    def switch_state(self):  
        if self.running:
            self.setIcon(self.icon_stopped)  
            self.running = False
            
        elif not self.running:
            self.setIcon(self.icon_running)  
            self.running = True         

    def move(self):
        time_to_move = 5
        while True:   
            if self.running == -1: break
            for i in range(time_to_move):             
                if self.running and i == time_to_move-1:    
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)
                time.sleep(1)                  
                if self.running == -1: break
           
#%% VERSION
VERSION = '1.0.0'

#%% MAIN           
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    sleeper = SleepPreventer()
    app.exec()