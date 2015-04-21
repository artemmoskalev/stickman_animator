'''
Created on Apr 12, 2015

@author: Artem
'''

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QWidget
from stickman.components.MainComponents import Canvas, ControlPanel
from stickman.components.Tools import ToolSet

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initGUI()
    
    def initGUI(self):
        self.resize(1200, 800)
        self.centerScreen()
        self.setWindowTitle('Stickman Animator v1.0')
        self.setWindowIcon(QIcon('stickman.png'))
        
        self.tools = ToolSet(self) 
        self.control_panel = ControlPanel(self, self.tools)
        self.canvas = Canvas(self)                       
        
        self.centerContents()
        
        self.show()
   
    def centerScreen(self):        
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        
    def centerContents(self):
        self.canvas.move(self.frameSize().width()/2-550, self.frameSize().height()/2-330)                        
        self.control_panel.move(self.frameSize().width()/2-550, self.frameSize().height()/2-390)
        self.tools.move(self.frameSize().width()/2-550, self.frameSize().height()/2+300)
              
    def resizeEvent(self, event):
        self.centerContents()