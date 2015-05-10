'''
Created on Apr 12, 2015

@author: Artem
'''

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QWidget, QPushButton, QFrame

from stickman.UI.Drawable import Canvas
from stickman.tools.WorldTools import WorldToolsPanel
from stickman.tools.StickmanTools import StickmanToolsPanel
from stickman.tools.AnimationTools import AnimationToolsPanel

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initGUI()
    
    def initGUI(self):
        self.setMinimumSize(1200, 800)
        self.resize(1200, 800)
        self.centerScreen()
        self.setWindowTitle('Stickman Animator v1.0')
        self.setWindowIcon(QIcon('resources/stickman.png'))
        
        self.tools = ToolSet(self) 
        self.canvas = Canvas(self, self.tools)  
        self.control_panel = ControlPanel(self, self.tools, self.canvas)                             
        
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
        
"""
    ---------------------------------------

    CLASS RESPONSIBLE FOR SWITCHING BETWEEN TOOLS
    
    ---------------------------------------

"""          
class ControlPanel(QFrame):
    
    def __init__(self, parent, tools, canvas):
        super().__init__(parent)
        self.tools = tools
        self.canvas = canvas
        self.initUI()
        
    def initUI(self):
        self.resize(454, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }                                
                            """
        
        """ all the control button switches are created from here """               
        world_tools_button = QPushButton('World Tools', self)
        world_tools_button.setCheckable(True)
        world_tools_button.resize(150, 30)
        world_tools_button.move(2, 2)        
        world_tools_button.setStyleSheet(button_stylesheet)
        world_tools_button.clicked.connect(self.pressControlPanelButton)
        
        stickman_tools_button = QPushButton('Stickman Tools', self)
        stickman_tools_button.setCheckable(True)
        stickman_tools_button.resize(150, 30)
        stickman_tools_button.move(152, 2)
        stickman_tools_button.setStyleSheet(button_stylesheet)
        stickman_tools_button.clicked.connect(self.pressControlPanelButton)
        
        animation_tools_button = QPushButton('Animation Tools', self)
        animation_tools_button.setCheckable(True)
        animation_tools_button.resize(150, 30)
        animation_tools_button.move(302, 2)
        animation_tools_button.setStyleSheet(button_stylesheet)
        animation_tools_button.clicked.connect(self.pressControlPanelButton)
            
        world_tools_button.click()
        
    """ listener method to switch the tools` set when tht control button is pressed"""
    def pressControlPanelButton(self):
        for child in self.children():
            child.setChecked(False)
            child.update()
            if child.text() == self.sender().text():
                child.setChecked(True)
                child.update()
                if self.sender().text() == "World Tools":
                    self.tools.showWorldTools()
                    self.canvas.showStickmenu()
                elif self.sender().text() == "Stickman Tools":
                    self.tools.showStickmanTools()
                    self.canvas.showStickmenu()
                else:
                    self.tools.showAnimationTools()
                    self.canvas.showFramemenu()
                       
                       
"""
    ---------------------------------------

    class which holds the references to the tool sets in order to switch them. can define their position and hide/show the tools
    
    ---------------------------------------

"""
class ToolSet():
    
    def __init__(self, parent):
        self.world_tools = WorldToolsPanel(parent)
        self.stickman_tools = StickmanToolsPanel(parent)
        self.animation_tools = AnimationToolsPanel(parent)
        self.hide()
        
    def move(self, x, y):
        self.world_tools.move(x, y)
        self.stickman_tools.move(x, y)
        self.animation_tools.move(x, y)
                
    def showWorldTools(self):
        self.hide()                
        self.world_tools.hideCreateDialog()
        self.world_tools.hideDeleteDialog()
        self.world_tools.show()
        
    def showStickmanTools(self):
        self.hide()
        self.stickman_tools.show()
        
    def showAnimationTools(self):
        self.hide()
        self.animation_tools.show() 
        
    def hide(self):
        self.world_tools.hide()
        self.stickman_tools.hide()
        self.animation_tools.hide()
        
