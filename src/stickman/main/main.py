'''
Created on Apr 11, 2015

@author: Artem
'''
import sys

from PyQt5.QtWidgets import QApplication
from stickman.components.Frames import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = MainWindow()    
    
    sys.exit(app.exec_())