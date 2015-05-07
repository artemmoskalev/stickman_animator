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
    
    sys.exit(app.exec_())