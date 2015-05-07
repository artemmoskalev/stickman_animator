'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QIcon, QSize, QLineEdit, QRect
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
        self.resize(700, 49)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFrameRect(QRect(0, 0, 184, 49))
        self.setLineWidth(1)
        
        component_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                                .QLineEdit {
                                    font-weight: bold;
                                    font-size: 24px;
                                }  
                            """
                        
        self.smile_button = QPushButton('', self)
        self.smile_button.setIcon(QIcon("resources/smile.png"))
        self.smile_button.setIconSize(QSize(35, 35))
        self.smile_button.resize(60, 45)
        self.smile_button.move(2, 2)        
        self.smile_button.setStyleSheet(component_stylesheet)
        self.smile_button.clicked.connect(self.changeExpression)
        self.smile_button.show()        

        self.sad_button = QPushButton('', self)
        self.sad_button.setIcon(QIcon("resources/sad.png"))
        self.sad_button.setIconSize(QSize(35, 35))
        self.sad_button.resize(60, 45)
        self.sad_button.move(62, 2)        
        self.sad_button.setStyleSheet(component_stylesheet)
        self.sad_button.clicked.connect(self.changeExpression)
        self.sad_button.show() 
        
        self.confused_button = QPushButton('', self)
        self.confused_button.setIcon(QIcon("resources/confused.png"))
        self.confused_button.setIconSize(QSize(35, 35))
        self.confused_button.resize(60, 45)
        self.confused_button.move(122, 2)        
        self.confused_button.setStyleSheet(component_stylesheet)
        self.confused_button.clicked.connect(self.changeExpression)
        self.confused_button.show() 
        
        self.say_text = QLineEdit(self)
        self.say_text.setStyleSheet(component_stylesheet)
        self.say_text.resize(300, 45)
        self.say_text.move(215, 2)
        
        self.say_left = QPushButton('', self)
        self.say_left.setIcon(QIcon("resources/say_left.png"))
        self.say_left.setIconSize(QSize(35, 35))
        self.say_left.resize(60, 45)
        self.say_left.move(520, 2)        
        self.say_left.setStyleSheet(component_stylesheet)
        self.say_left.clicked.connect(self.sayLeft)
        
        self.say_right = QPushButton('', self)
        self.say_right.setIcon(QIcon("resources/say_right.png"))
        self.say_right.setIconSize(QSize(35, 35))
        self.say_right.resize(60, 45)
        self.say_right.move(580, 2)   
        self.say_right.setStyleSheet(component_stylesheet)
        self.say_right.clicked.connect(self.sayRight)
        
        self.say_exit = QPushButton('', self)
        self.say_exit.setIcon(QIcon("resources/exit.png"))
        self.say_exit.setIconSize(QSize(35, 35))
        self.say_exit.resize(60, 45)
        self.say_exit.move(640, 2)   
        self.say_exit.setStyleSheet(component_stylesheet)
        self.say_exit.clicked.connect(self.sayClear)
        
    def sayLeft(self):
        search = getWorld().getActive()
        if search != None:
            search.sayLeft(self.say_text.text())
        self.say_text.setText("")
    def sayRight(self):
        search = getWorld().getActive()
        if search != None:
            search.sayRight(self.say_text.text())
        self.say_text.setText("")
    def sayClear(self):
        search = getWorld().getActive()
        if search != None:
            search.sayRemove()
        self.say_text.setText("")
    
    def changeExpression(self):
        search = getWorld().getActive()
        if search != None:
            if self.sender() == self.smile_button:
                search.setHappy()
            elif self.sender() == self.sad_button:
                search.setSad()
            else:
                search.setConfused()
