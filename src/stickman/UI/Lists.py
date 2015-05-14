'''
Created on May 13, 2015

@author: Artem
'''

from PyQt5.Qt import QMessageBox, QWidget, QPushButton, QSize

from stickman.tools.Components import FrameMap
from stickman.model.World import getWorld, World

from stickman.UI.AssetManager import assets

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
                       
        getWorld().addListener(self.onStickmanListener)
        
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
        self.scroll_up_button.setIcon(assets.up)
        self.scroll_up_button.setIconSize(QSize(50, 25))
        self.scroll_up_button.resize(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT)        
        self.scroll_up_button.move(0, StickmanList.BUTTON_HEIGHT*11 + 20)
        self.scroll_up_button.setStyleSheet(scroll_button_style)
        self.scroll_up_button.clicked.connect(self.scrollListUp)
        self.scroll_up_button.hide()
            
        self.scroll_down_button = QPushButton("", self)
        self.scroll_down_button.setIcon(assets.down)
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
        elif operation == World.ACTIVE_EVENT:
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
        self.scroll_up_button.setIcon(assets.up)
        self.scroll_up_button.setIconSize(QSize(50, 25))
        self.scroll_up_button.resize(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT)        
        self.scroll_up_button.move(0, StickmanList.BUTTON_HEIGHT*11 + 20)
        self.scroll_up_button.setStyleSheet(scroll_button_style)
        self.scroll_up_button.clicked.connect(self.scrollListUp)
        self.scroll_up_button.hide()
            
        self.scroll_down_button = QPushButton("", self)
        self.scroll_down_button.setIcon(assets.down)
        self.scroll_down_button.setIconSize(QSize(50, 25))
        self.scroll_down_button.resize(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT)
        self.scroll_down_button.move(StickmanList.BUTTON_WIDTH/2, StickmanList.BUTTON_HEIGHT*11 + 20)
        self.scroll_down_button.setStyleSheet(scroll_button_style)
        self.scroll_down_button.clicked.connect(self.scrollListDown)
        self.scroll_down_button.hide()
        
        self.start_index = 0
    
    """ Methods for changing the frames on the FrameList """
    def addNewFrame(self, frame):
        button = QPushButton("", self)
        button.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT)
        button.clicked.connect(self.onMousePressed)
        button.show()
        self.buttons[button] = frame
        if len(self.buttons) > 10:
            self.start_index = len(self.buttons) - 10
        self.rearrangeButtons()
    
    def deleteFrame(self, caller):
        if not self.buttons.active == None:
            response = QMessageBox.question(caller, 'Frame Remove Message', "Are you sure you want to delete this frame?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if response == QMessageBox.Yes:
                self.buttons.active.setParent(None)
                del self.buttons[self.buttons.active]
                if self.start_index > 0:
                    self.start_index = self.start_index-1
        self.rearrangeButtons()
    
    def removeAllFrames(self):
        self.buttons.active = None
        for button in self.buttons.keys().copy():
            button.setParent(None)
            del self.buttons[button]
        self.start_index = 0
        self.rearrangeButtons()
    
    def copyFrame(self):
        if not self.buttons.active == None:            
            button = QPushButton("", self)
            button.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT)
            button.clicked.connect(self.onMousePressed)
            button.show()
            
            index = self.buttons.index(self.buttons.active)  
            copy_frame = getWorld().getFrame()
            copy_frame.time = self.buttons[self.buttons.active].time
            self.buttons.insertAt(index+1, button, copy_frame)
            if len(self.buttons) > 10:
                self.start_index = self.start_index + 1
            self.rearrangeButtons()
    
    def changeFrameTime(self, time):
        if not self.buttons.active == None:
            self.buttons[self.buttons.active].time = time
            self.rearrangeButtons()
    
    """ Convenience methods for frame retrieval used by the animation player and some buttons """            
    def getActiveFrame(self):
        if not self.buttons.active == None:
            return (self.buttons.active, self.buttons[self.buttons.active])
        else:
            return None    
    def getFirstFrame(self):
        first_button = self.buttons.first()
        if not first_button == None:
            return self.buttons[first_button]
        else:
            return None    
    def getNextFrame(self, frame):
        return self.buttons.nextValue(frame)
        
    def getAllFrames(self):
        return self.buttons.frames        
    
    """ fixes button positions on the stickmen list after button addition or removal. 
        activates/deactivates buttons depending on which stickman is active.
        In case there are more than 10 buttons, shows scrolling buttons. Controls which buttons are hidden and which are shown. """            
    def rearrangeButtons(self):    
        i = 0
        for button in self.buttons.keys():
            if i == 0:
                button.setText("Frame " + str(i+1) + " : " + "0.0s")
            else:
                button.setText("Frame " + str(i+1) + " : " + str("%0.1f" % (self.buttons[button].time)) + "s") #makes up for removed frames, restoring the naming order
               
            if i < self.start_index:
                button.hide()
            elif i > (self.start_index + 9):
                button.hide()
            else:
                button.show()
                button.move(0, (i-self.start_index)*45)
                if button == self.buttons.active:
                    button.setStyleSheet(self.button_style_active)
                else:
                    button.setStyleSheet(self.button_style_passive)
            i = i+1 
        #part which whows or hides up-down scroll buttons    
        if len(self.buttons) > 10:
            self.scroll_up_button.show()
            self.scroll_down_button.show()
        else:
            self.scroll_up_button.hide()
            self.scroll_down_button.hide()
            
        self.parent().tools.animation_tools.showButtonBlock()
                
        
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
        #sets the world to a copy of the current contents, preserving frame from future changes
        if self.sender() == self.buttons.active:
            self.buttons.active = None   
            getWorld().copyWorld()     
        #sets the world to the current frame contents          
        else:
            open_frame = self.buttons[self.sender()]
            getWorld().setWorldFrom(open_frame)
            self.buttons.active = self.sender()        
        self.rearrangeButtons()
                    
