'''
Created on Apr 12, 2015

@author: Artem
'''

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.Qt import QWidget, QPushButton, QLabel, QFrame, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

from stickman.model.World import getWorld, World
from stickman.UI.Lists import StickmanList, FrameList
from stickman.tools.WorldTools import WorldToolsPanel
from stickman.tools.StickmanTools import StickmanToolsPanel
from stickman.tools.AnimationTools import AnimationToolsPanel

from stickman.UI.AssetManager import assets

class MainWindow(QWidget):    
    
    EXTENSION = 60
    LEFT_PADDING = 550
    
    CANVAS_RELATIVE_Y = -330
    PANEL_RELATIVE_Y = -370
    TOOLS_RELATIVE_Y = 280
    
    def __init__(self):
        super().__init__()
        self.initGUI()
    
    def initGUI(self):
        self.setMinimumSize(World.WIDTH + MainWindow.EXTENSION, World.HEIGHT + MainWindow.EXTENSION*2)
        self.resize(World.WIDTH + MainWindow.EXTENSION, World.HEIGHT + MainWindow.EXTENSION*2)
        self.centerScreen()
        self.setWindowTitle('Stickman Animator v1.0')
        
        self.setWindowIcon(assets.stickman)
        
        self.canvas = Canvas(self)  
        self.tools = ToolSet(self) 
        self.control_panel = ControlPanel(self, self.tools)                       
        
        self.centerContents()
        
        self.show()
   
    def centerScreen(self):        
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        
    def centerContents(self):
        self.canvas.move(self.frameSize().width()/2 - MainWindow.LEFT_PADDING, self.frameSize().height()/2 + MainWindow.CANVAS_RELATIVE_Y)                        
        self.control_panel.move(self.frameSize().width()/2 - MainWindow.LEFT_PADDING, self.frameSize().height()/2 + MainWindow.PANEL_RELATIVE_Y)
        self.tools.move(self.frameSize().width()/2 - MainWindow.LEFT_PADDING, self.frameSize().height()/2 + MainWindow.TOOLS_RELATIVE_Y)
              
    def resizeEvent(self, event):
        self.centerContents()
        
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
                elif self.sender().text() == "Stickman Tools":
                    self.tools.showStickmanTools()
                else:
                    self.tools.showAnimationTools()
                       
"""
    ---------------------------------------

    CLASS RESPONSIBLE FOR DELEGATING THE DRAWING THE STICKMEN AND SOME CONTROLS
    
    ---------------------------------------

"""            
class Canvas(QFrame):   
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
        self.timer = QTimer(self)       
        self.timer.timeout.connect(self.update)
        self.timer.start(25)       
        
    def initUI(self):
        self.resize(World.WIDTH, World.HEIGHT)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("background-color:#FFFFFF;")     
    
        label_stylesheet = """
                                .QLabel {
                                    font-weight: bold;
                                    font-size: 21px;
                                    color: red;
                                    border: 1px solid red;
                                }
                            """
    
        self.message = QLabel("FRAME MODIFIED!", self)
        self.message.setStyleSheet(label_stylesheet)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.resize(StickmanList.BUTTON_WIDTH, StickmanList.BUTTON_HEIGHT)
        self.message.move(World.WIDTH-StickmanList.BUTTON_WIDTH-15, World.HEIGHT-StickmanList.BUTTON_HEIGHT*1.5)
        self.message.hide()
    
    """ Draw and listener methods which are dispatched to the World """
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)       
        
        getWorld().draw(painter)            
        
        painter.end()      
    
    def showMessage(self):
        self.message.show()
    def hideMessage(self):
        self.message.hide()
    
    def mousePressEvent(self, event):
        getWorld().mousePressed(event.x(), event.y())   
        
    def mouseReleaseEvent(self, event):
        getWorld().mouseReleased(event.x(), event.y())    
    
    def mouseMoveEvent(self, event):
        getWorld().mouseMoved(event.x(), event.y())  

                   
"""
    ---------------------------------------

    class which holds the references to the tool sets in order to switch them. can define their position and hide/show the tools
    
    ---------------------------------------

"""
class ToolSet():
        
    MENU_POSITION_X = 845
    MENU_POSITION_Y = -595      
    
    def __init__(self, parent):
        self.world_tools = WorldToolsPanel(parent)
        self.stickman_tools = StickmanToolsPanel(parent, self)
        self.animation_tools = AnimationToolsPanel(parent, self)
        self.hide()
        
        self.stickmenu = StickmanList(parent)
        self.framemenu = FrameList(parent)   
        self.framemenu.hide()
        
    """ methods for function panel buttons """   
    def move(self, x, y):
        self.world_tools.move(x, y)
        self.stickman_tools.move(x, y)
        self.animation_tools.move(x, y)
        self.stickmenu.move(x + ToolSet.MENU_POSITION_X, y + ToolSet.MENU_POSITION_Y)
        self.framemenu.move(x + ToolSet.MENU_POSITION_X, y + ToolSet.MENU_POSITION_Y)                    
                                    
    def showWorldTools(self):
        self.hide()                
        self.world_tools.hideCreateDialog()
        self.world_tools.hideDeleteDialog()
        self.world_tools.show()
        self.showStickmenu()
        
    def showStickmanTools(self):
        self.hide()
        self.stickman_tools.show()
        self.showStickmenu()
        
    def showAnimationTools(self):
        self.hide()
        self.animation_tools.show() 
        self.animation_tools.showButtonBlock()
        self.showFramemenu()   
        
    #internal method. Used only from this class
    def hide(self):
        self.world_tools.hide()
        self.stickman_tools.hide()
        self.animation_tools.hide()   
    
    """ methods for on-canvas lists """
    def showStickmenu(self):
        self.stickmenu.show()
        self.framemenu.hide()
        
    def showFramemenu(self):
        self.stickmenu.hide()
        self.framemenu.show()      
        
    