'''
Created on Apr 21, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame
         
"""
    ---------------------------------------

    CLASS RESPONSIBLE FOR SWITCHING BETWEEN TOOLS
    
    ---------------------------------------

"""          
class ControlPanel(QFrame):
    
    def __init__(self, parent, tools):
        super().__init__(parent)
        self.tools = tools
        self.initUI()
        
    def initUI(self):
        self.resize(604, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#FFFFFF;
                                }
                            """
        
        """ all the control button switches are created from here """               
        stickman_tools_button = QPushButton('Stickman Tools', self)
        stickman_tools_button.setCheckable(True)
        stickman_tools_button.resize(150, 30)
        stickman_tools_button.move(2, 2)        
        stickman_tools_button.setStyleSheet(button_stylesheet)
        stickman_tools_button.clicked.connect(self.pressControlPanelButton)
        
        animation_tools_button = QPushButton('Animation Tools', self)
        animation_tools_button.setCheckable(True)
        animation_tools_button.resize(150, 30)
        animation_tools_button.move(152, 2)
        animation_tools_button.setStyleSheet(button_stylesheet)
        animation_tools_button.clicked.connect(self.pressControlPanelButton)
        
        io_tools_button = QPushButton('Input/Output Tools', self)
        io_tools_button.setCheckable(True)
        io_tools_button.resize(150, 30)
        io_tools_button.move(302, 2)
        io_tools_button.setStyleSheet(button_stylesheet)
        io_tools_button.clicked.connect(self.pressControlPanelButton)
        
        other_tools_button = QPushButton('Other Tools', self)
        other_tools_button.setCheckable(True)       
        other_tools_button.resize(150, 30)
        other_tools_button.move(452, 2)
        other_tools_button.setStyleSheet(button_stylesheet)        
        other_tools_button.clicked.connect(self.pressControlPanelButton)
    
        stickman_tools_button.click()
        
    """ listener method to switch the tools` set when tht control button is pressed"""
    def pressControlPanelButton(self):
        for child in self.children():
            child.setChecked(False)
            child.update()
            if child.text() == self.sender().text():
                child.setChecked(True)
                child.update()
                if self.sender().text() == "Stickman Tools":
                    self.tools.showStickmanTools()
                elif self.sender().text() == "Animation Tools":
                    self.tools.showAnimationTools()
                elif self.sender().text() == "Input/Output Tools":
                    self.tools.showIOTools()
                else:
                    self.tools.showOtherTools()
   
   
"""
    ---------------------------------------

    CLASS RESPONSIBLE FOR DRAWING THE STICKMEN AND SOME CONTROLS
    
    ---------------------------------------

"""            
class Canvas(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(1100, 600)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("background-color:#FFFFFF;")          