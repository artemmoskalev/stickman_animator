'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QSize, QLineEdit, QRect
from stickman.model.World import getWorld

from stickman.UI.AssetManager import assets

"""
    ---------------------------------------

    ClASS RESPONSIBLE ANIMATION OF STICKMEN
    
    ---------------------------------------

""" 
class StickmanToolsPanel(QFrame):
    
    WIDTH = 1100
    HEIGHT = 45
    
    FRAME_SIZE_X = 180
    FRAME_WIDTH = 1
    FRAME_MARGIN = 2
    
    ICON_SIZE = 35
    ICON_BUTTON_WIDTH = 60
    INPUT_TEXT_WIDTH = 300
    INPUT_START_X = 213
    SAY_BLOCK_X = 520
    PHOTO_BUTTON_WIDTH = 240
    PHOTO_BUTTON_X = 858
    
    def __init__(self, parent, tools):
        super().__init__(parent)
        self.tools = tools
        self.initUI()
        
    def initUI(self):
        self.resize(StickmanToolsPanel.WIDTH, StickmanToolsPanel.HEIGHT + StickmanToolsPanel.FRAME_MARGIN*2)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFrameRect(QRect(0, 0, StickmanToolsPanel.FRAME_SIZE_X + StickmanToolsPanel.FRAME_MARGIN*2, StickmanToolsPanel.HEIGHT + StickmanToolsPanel.FRAME_MARGIN*2))
        self.setLineWidth(StickmanToolsPanel.FRAME_WIDTH)
        
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
        self.smile_button.setIcon(assets.smile)
        self.smile_button.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.smile_button.resize(StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.smile_button.move(StickmanToolsPanel.FRAME_MARGIN, StickmanToolsPanel.FRAME_MARGIN)        
        self.smile_button.setStyleSheet(component_stylesheet)
        self.smile_button.clicked.connect(self.changeExpression)
        self.smile_button.show()        

        self.sad_button = QPushButton('', self)
        self.sad_button.setIcon(assets.sad)
        self.sad_button.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.sad_button.resize(StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.sad_button.move(StickmanToolsPanel.FRAME_MARGIN + StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.FRAME_MARGIN)        
        self.sad_button.setStyleSheet(component_stylesheet)
        self.sad_button.clicked.connect(self.changeExpression)
        self.sad_button.show() 
        
        self.confused_button = QPushButton('', self)
        self.confused_button.setIcon(assets.confused)
        self.confused_button.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.confused_button.resize(StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.confused_button.move(StickmanToolsPanel.FRAME_MARGIN + StickmanToolsPanel.ICON_BUTTON_WIDTH*2, StickmanToolsPanel.FRAME_MARGIN)        
        self.confused_button.setStyleSheet(component_stylesheet)
        self.confused_button.clicked.connect(self.changeExpression)
        self.confused_button.show() 
        
        self.say_text = QLineEdit(self)
        self.say_text.setStyleSheet(component_stylesheet)
        self.say_text.resize(StickmanToolsPanel.INPUT_TEXT_WIDTH, StickmanToolsPanel.HEIGHT)
        self.say_text.move(StickmanToolsPanel.FRAME_MARGIN + StickmanToolsPanel.INPUT_START_X, StickmanToolsPanel.FRAME_MARGIN)
        
        self.say_left = QPushButton('', self)
        self.say_left.setIcon(assets.say_left)
        self.say_left.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.say_left.resize(StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.say_left.move(StickmanToolsPanel.SAY_BLOCK_X, StickmanToolsPanel.FRAME_MARGIN)        
        self.say_left.setStyleSheet(component_stylesheet)
        self.say_left.clicked.connect(self.sayLeft)
        
        self.say_right = QPushButton('', self)
        self.say_right.setIcon(assets.say_right)
        self.say_right.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.say_right.resize(StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.say_right.move(StickmanToolsPanel.SAY_BLOCK_X + StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.FRAME_MARGIN)   
        self.say_right.setStyleSheet(component_stylesheet)
        self.say_right.clicked.connect(self.sayRight)
        
        self.say_exit = QPushButton('', self)
        self.say_exit.setIcon(assets.exit)
        self.say_exit.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.say_exit.resize(StickmanToolsPanel.ICON_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.say_exit.move(StickmanToolsPanel.SAY_BLOCK_X + StickmanToolsPanel.ICON_BUTTON_WIDTH*2, StickmanToolsPanel.FRAME_MARGIN)   
        self.say_exit.setStyleSheet(component_stylesheet)
        self.say_exit.clicked.connect(self.sayClear)
        
        self.photo = QPushButton('', self)
        self.photo.setIcon(assets.camera)
        self.photo.setIconSize(QSize(StickmanToolsPanel.ICON_SIZE, StickmanToolsPanel.ICON_SIZE))
        self.photo.resize(StickmanToolsPanel.PHOTO_BUTTON_WIDTH, StickmanToolsPanel.HEIGHT)
        self.photo.move(StickmanToolsPanel.PHOTO_BUTTON_X, StickmanToolsPanel.FRAME_MARGIN)
        self.photo.setStyleSheet(component_stylesheet)
        self.photo.clicked.connect(self.makePhoto)
        
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
    
    def makePhoto(self):
        self.tools.framemenu.addNewFrame(getWorld().getFrame())
    