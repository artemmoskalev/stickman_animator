'''
Created on Apr 11, 2015

@author: Artem
'''
import sys

from PyQt5.QtWidgets import QApplication
from stickman.UI.Frames import MainWindow

from stickman.model.World import getWorld

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = MainWindow()    
    getWorld().createStickman("artemka", 500, 100)
    getWorld().createStickman("artemka1", 500, 100)
    getWorld().createStickman("artemka2", 500, 100)
    getWorld().createStickman("artemka3", 500, 100)
    getWorld().createStickman("artemka4", 500, 100)
    getWorld().createStickman("artemka5", 500, 100)
    getWorld().createStickman("artemka6", 500, 100)
    getWorld().createStickman("artemka7", 500, 100)
    getWorld().createStickman("artemka8", 500, 100)
    getWorld().createStickman("artemka9", 500, 100)
    getWorld().createStickman("artemka11", 500, 100)
    getWorld().createStickman("ivan", 500, 100)
    getWorld().createStickman("Bors", 500, 100)
    
    sys.exit(app.exec_())