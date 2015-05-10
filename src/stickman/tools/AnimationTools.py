'''
Created on Apr 25, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QIcon, QSize, QRect

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR SAVING AND LOADING ANIMATIONS
    
    ---------------------------------------

"""       
class AnimationToolsPanel(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(1100, 49)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFrameRect(QRect(0, 0, 304, 34))
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
                        
        self.save_animation = QPushButton('Save Animation', self)
        self.save_animation.resize(150, 30)
        self.save_animation.move(2, 2)        
        self.save_animation.setStyleSheet(button_stylesheet)
       
        self.load_animation = QPushButton('Load Animation', self)
        self.load_animation.resize(150, 30)
        self.load_animation.move(152, 2)        
        self.load_animation.setStyleSheet(button_stylesheet)
        
        self.time_button = QPushButton('', self)
        self.time_button.setIcon(QIcon("resources/time.png"))
        self.time_button.setIconSize(QSize(35, 35))
        self.time_button.resize(60, 45)
        self.time_button.move(918, 2)        
        self.time_button.setStyleSheet(button_stylesheet)
        #self.time_button.clicked.connect(self.changeExpression)
        self.time_button.show()        

        self.copy_button = QPushButton('', self)
        self.copy_button.setIcon(QIcon("resources/copy.png"))
        self.copy_button.setIconSize(QSize(35, 35))
        self.copy_button.resize(60, 45)
        self.copy_button.move(978, 2)        
        self.copy_button.setStyleSheet(button_stylesheet)
        self.copy_button.clicked.connect(self.copyFrameListener)
        self.copy_button.show() 
        
        self.delete_button = QPushButton('', self)
        self.delete_button.setIcon(QIcon("resources/delete.png"))
        self.delete_button.setIconSize(QSize(35, 35))
        self.delete_button.resize(60, 45)
        self.delete_button.move(1038, 2)        
        self.delete_button.setStyleSheet(button_stylesheet)
        self.delete_button.clicked.connect(self.deleteListener)
        self.delete_button.show() 
        
    def deleteListener(self):
        self.parent().canvas.deleteFrames()
    def copyFrameListener(self):
        self.parent().canvas.copyFrame()
    
    