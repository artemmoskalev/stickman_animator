'''
Created on Apr 21, 2015

@author: Artem
'''

from PyQt5.Qt import QApplication, QWidget, QPushButton, QFrame, QTimer, QIcon, QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

from stickman.model.World import getWorld, World
   
"""
    ---------------------------------------

    CLASS RESPONSIBLE FOR DELEGATING THE DRAWING THE STICKMEN AND SOME CONTROLS
    
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
        
        self.stickmenu = StickmanList(self)       
        self.stickmenu.move(Canvas.MENU_POSITION_X, Canvas.MENU_POSITION_Y)
        
        self.framemenu = FrameList(self)       
        self.framemenu.move(Canvas.MENU_POSITION_X, Canvas.MENU_POSITION_Y)
        self.framemenu.hide()
                
    def initUI(self):
        self.resize(1100, 600)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("background-color:#FFFFFF;")    
    
    def showStickmenu(self):
        self.stickmenu.show()
        self.framemenu.hide()
        
    def showFramemenu(self):
        self.stickmenu.hide()
        self.framemenu.show()
    
    """ Methods erlated to frame list """
    def createNewFrame(self):
        self.framemenu.addNewFrame()
    
    def deleteFrames(self):
        self.framemenu.deleteFrames()
        
    def copyFrame(self):
        self.framemenu.copyFrame()
    
    """ Draw and listener methods """
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


"""
    ---------------------------------------

    COMPONENT CLASS FOR THE LIST OF CURRENT STICKMEN IN THE WORLD
    
    ---------------------------------------

"""   
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
        
        self.start_index = 0    #required to track the first element in the list which is shown
        
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
    
"""
    ---------------------------------------

    COMPONENT CLASS FOR THE LIST OF FRAMES CURRENTLY SHOT IN THE WORLD
    
    ---------------------------------------

"""   
class FrameList(QWidget):
    
    BUTTON_WIDTH = 240
    BUTTON_HEIGHT = 40
    
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(FrameList.BUTTON_WIDTH, FrameList.BUTTON_HEIGHT*12 + 20)
        self.initUI()
                
    def initUI(self):
        self.buttons = FrameMap()
        self.active = list()
        
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
    
    """ Methods for changing the frames on the FrameList. Called from the Canvas class"""
    def addNewFrame(self):
        button = QPushButton("", self)
        button.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT)
        button.clicked.connect(self.onMousePressed)
        button.show()
        self.buttons[button] = Frame()
        if len(self.buttons) > 10:
            self.start_index = len(self.buttons) - 10
        self.active[:] = []
        self.active.append(button)
        self.rearrangeButtons()
    
    def deleteFrames(self):
        for button in self.active.copy():
            self.active.remove(button)
            del self.buttons[button]
            button.setParent(None)
            if self.start_index > 0:
                self.start_index = self.start_index-1
        self.rearrangeButtons()
    
    def copyFrame(self):
        if len(self.active) == 1:            
            button = QPushButton("", self)
            button.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT)
            button.clicked.connect(self.onMousePressed)
            button.show()
            
            index = self.buttons.index(self.active[0])
            self.buttons.insertAt(index, button, Frame())
            if len(self.buttons) > 10:
                self.start_index = self.start_index + 1
            self.rearrangeButtons()
                        
    """ fixes button positions on the stickmen list after button addition or removal. 
        activates/deactivates buttons depending on which stickman is active.
        In case there are morre than 10 buttons, shows scrolling buttons. Controls which buttons are hidden and which are shown. """            
    def rearrangeButtons(self):    
        i = 0
        for button in self.buttons.keys():
            button.setText("Frame " + str(i+1)) #makes up for removed frames, restoring the naming order
            if i < self.start_index:
                button.hide()
            elif i > (self.start_index + 9):
                button.hide()
            else:
                button.show()
                button.move(0, (i-self.start_index)*45)
                if button in self.active:
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
    
    """ listener method used to switch between currently present frames """
    def onMousePressed(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            if self.sender() not in self.active:
                self.active.append(self.sender())
            else:
                self.active.remove(self.sender())                
        else:
            self.active[:] = []
            self.active.append(self.sender())
        self.rearrangeButtons()

"""
    ---------------------------
    CLASS FOR STORING MAPPINGS BETWEEN BUTTONS AND FRAMES. SIMPLIFIED VERSION OF DICT
    ---------------------------
"""
class FrameMap():
    
    def __init__(self):
        self.buttons = list()
        self.frames = list()
    
    def __delitem__(self, key):
        index = self.buttons.index(key)
        self.buttons.remove(key)
        del self.frames[index]
        
    def __getitem__(self, key):
        return self.frames(self.buttons.index(key))
        
    def __setitem__(self, key, value):
        self.buttons.append(key)
        self.frames.append(value)
    
    def __len__(self):
        return len(self.buttons)
    
    def keys(self):
        return self.buttons
    
    def index(self, key):
        return self.buttons.index(key)
    
    def insertAt(self, index, key, value):
        self.buttons.insert(index, key)
        self.frames.insert(index, value)
        
"""
    ---------------------------
    CLASS RESPONSIBLE FOR STORING FRAME DATA
    ---------------------------
"""
class Frame():
    
    def __init__(self):
        pass

