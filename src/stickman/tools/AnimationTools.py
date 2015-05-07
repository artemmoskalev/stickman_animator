'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QIcon, QSize
from stickman.model.World import getWorld

"""
    ---------------------------------------

    ClASS RESPONSIBLE ANIMATION OF STICKMEN
    
    ---------------------------------------

""" 
class AnimationTools(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(124, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                            """
                        
        self.smile_button = QPushButton('', self)
        self.smile_button.setIcon(QIcon("resources/smile.png"))
        self.smile_button.setIconSize(QSize(22, 22))
        self.smile_button.resize(40, 30)
        self.smile_button.move(2, 2)        
        self.smile_button.setStyleSheet(button_stylesheet)
        self.smile_button.clicked.connect(self.changeExpression)
        self.smile_button.show()        

        self.sad_button = QPushButton('', self)
        self.sad_button.setIcon(QIcon("resources/sad.png"))
        self.sad_button.setIconSize(QSize(22, 22))
        self.sad_button.resize(40, 30)
        self.sad_button.move(42, 2)        
        self.sad_button.setStyleSheet(button_stylesheet)
        self.sad_button.clicked.connect(self.changeExpression)
        self.sad_button.show() 
        
        self.confused_button = QPushButton('', self)
        self.confused_button.setIcon(QIcon("resources/confused.png"))
        self.confused_button.setIconSize(QSize(22, 22))
        self.confused_button.resize(40, 30)
        self.confused_button.move(82, 2)        
        self.confused_button.setStyleSheet(button_stylesheet)
        self.confused_button.clicked.connect(self.changeExpression)
        self.confused_button.show() 
        
    def changeExpression(self):
        search = getWorld().getActive()
        if search != None:
            if self.sender() == self.smile_button:
                search.setHappy()
            elif self.sender() == self.sad_button:
                search.setSad()
            else:
                search.setConfused()
