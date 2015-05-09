'''
Created on Apr 21, 2015

@author: Artem
'''

from PyQt5.Qt import QWidget, QPushButton, QFrame, QTimer, QIcon, QSize
from PyQt5.QtGui import QPainter

from stickman.model.World import getWorld, World

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
                else:
                    self.tools.showIOTools()
                       
   
"""
    ---------------------------------------

    CLASS RESPONSIBLE FOR DRAWING THE STICKMEN AND SOME CONTROLS
    
    ---------------------------------------

"""            
class Canvas(QFrame):
    
    MENU_POSITION_X = 850
    MENU_POSITION_Y = 20
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
        self.timer = QTimer(self)       
        self.timer.timeout.connect(self.update)
        self.timer.start(25)
        
        self.menu = StickmanList(self)       
        self.menu.move(Canvas.MENU_POSITION_X, Canvas.MENU_POSITION_Y)
        
    def initUI(self):
        self.resize(1100, 600)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("background-color:#FFFFFF;")    
        
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)       
        
        getWorld().draw(painter)            
        
        painter.end()      
    
    def mousePressEvent(self, event):
        getWorld().mousePressed(event.x(), event.y())   
        
    def mouseReleaseEvent(self, event):
        getWorld().mouseReleased(event.x(), event.y())    
    
    def mouseMoveEvent(self, event):
        getWorld().mouseMoved(event.x(), event.y())  

class StickmanList(QWidget):
    
    BUTTON_WIDTH = 240
    BUTTON_HEIGHT = 40
    
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT*12 + 20)
        self.initUI()        
                
    def initUI(self):
        self.buttons = list()
        
        self.button_style_passive = """
                          .QPushButton {
                              font-weight: bold;
                              font-size: 20px;
                              background-color:#D3D3D3;
                              border: 1px solid black;
                          }
                      """
        self.button_style_active = """
                          .QPushButton {
                              font-weight: bold;
                              font-size: 20px;
                              background-color:#B4B4B4;
                              border: 2px solid black;
                          }
                      """
                       
        getWorld().addStickmanListener(self.onStickmanListener)
        
        """ These are the buttons to control list of names scrolling. start_index is the index which points to the 
            first entry in the button list which is currently shown at the top of the visual list. """
        scroll_button_style = """
                                 .QPushButton {
                                      font-weight: bold;
                                      font-size: 20px;
                                      background-color:#D3D3D3;
                                  }
                                  .QPushButton:pressed {
                                      background-color:#B4B4B4;
                                  }       
                               """
        
        self.scroll_up_button = QPushButton("", self)
        self.scroll_up_button.setIcon(QIcon("resources/up.png"))
        self.scroll_up_button.setIconSize(QSize(50, 25))
        self.scroll_up_button.resize(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT)        
        self.scroll_up_button.move(0, StickmanList.BUTTON_HEIGHT*11 + 20)
        self.scroll_up_button.setStyleSheet(scroll_button_style)
        self.scroll_up_button.clicked.connect(self.scrollListUp)
        self.scroll_up_button.hide()
            
        self.scroll_down_button = QPushButton("", self)
        self.scroll_down_button.setIcon(QIcon("resources/down.png"))
        self.scroll_down_button.setIconSize(QSize(50, 25))
        self.scroll_down_button.resize(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT)
        self.scroll_down_button.move(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT*11 + 20)
        self.scroll_down_button.setStyleSheet(scroll_button_style)
        self.scroll_down_button.clicked.connect(self.scrollListDown)
        self.scroll_down_button.hide()
        
        self.start_index = 0
        
    """ fixes button positions on the stickmen list after button addition or removal. 
        activates/deactivates buttons depending on which stickman is active.
        In case there are morre than 10 buttons, shows scrolling buttons. Controls which buttons are hidden and which are shown. """            
    def rearrangeButtons(self):    
        i = 0
        for button in self.buttons:
            if i < self.start_index:
                button.hide()
            elif i > (self.start_index + 9):
                button.hide()
            else:
                button.show()
                button.move(0, (i-self.start_index)*45)
                if getWorld().isActive(button.text()):
                    button.setStyleSheet(self.button_style_active)
                else:
                    button.setStyleSheet(self.button_style_passive)
            i = i+1 
            
        if len(self.buttons) > 10:
            self.scroll_up_button.show()
            self.scroll_down_button.show()
        else:
            self.scroll_up_button.hide()
            self.scroll_down_button.hide()
    
    def scrollListUp(self):
        if self.start_index > 0:
            self.start_index = self.start_index - 1
            self.rearrangeButtons()
                       
    def scrollListDown(self):
        if self.start_index < len(self.buttons)-10:
            self.start_index = self.start_index + 1
            self.rearrangeButtons()
                
    """ listener method which create on-screen buttons with stickman names or remove them. It redraws buttons if active state changes. Called from the World class """
    def onStickmanListener(self, name, operation):
        if operation == World.ADD_EVENT:
            button = QPushButton(name, self)
            button.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT)
            button.clicked.connect(self.onMousePressed)
            button.show()
            self.buttons.insert(0, button)    
            self.start_index = 0    
            self.rearrangeButtons()
        elif operation == World.REMOVE_EVENT:
            for button in self.buttons:
                if button.text() == name:
                    self.buttons.remove(button)
                    button.setParent(None)
                    if self.start_index > 0:
                        self.start_index = self.start_index - 1
                    self.rearrangeButtons()
        else:
            self.rearrangeButtons()
        
    """ listener method used to switch active states of stickmen """
    def onMousePressed(self):
        getWorld().setActive(self.sender().text())
    
        