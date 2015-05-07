'''
Created on Apr 25, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR SAVING AND LOADING ANIMATIONS
    
    ---------------------------------------

"""       
class IOTools(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(304, 34)
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
                        
        save_animation = QPushButton('Save Animation', self)
        save_animation.resize(150, 30)
        save_animation.move(2, 2)        
        save_animation.setStyleSheet(button_stylesheet)
       
        load_animation = QPushButton('Load Animation', self)
        load_animation.resize(150, 30)
        load_animation.move(152, 2)        
        load_animation.setStyleSheet(button_stylesheet)
