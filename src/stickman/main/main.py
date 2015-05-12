'''
Created on Apr 11, 2015

@author: Artem
'''
import sys

from PyQt5.QtWidgets import QApplication

from stickman.model.World import getWorld
from stickman.UI.MainComponents import MainWindow

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    
    w = MainWindow()    
    getWorld().createStickman("artemka", 500, 100)
    
    sys.exit(app.exec_())