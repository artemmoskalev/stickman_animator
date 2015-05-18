'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QRect, QFileDialog
from stickman.tools.Components import InputLine
from stickman.model.World import getWorld

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR CREATION AND DELETION OF STICKMEN
    
    ---------------------------------------

"""
class WorldToolsPanel(QFrame):
    
    FRAME_WIDTH = 1
    FRAME_MARGIN = 2
    TOOLS_WIDTH = 600
    TOOLS_HEIGHT = 30
    
    INPUT_WIDTH = 585    
    BUTTON_WIDTH = 150    
    
    STICKMAN_X = 300
    STICKMAN_Y = 100
    STICKMAN_NAME_MAX_LENGTH = 15   
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):        
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(WorldToolsPanel.FRAME_WIDTH)
        
        self.resize(WorldToolsPanel.TOOLS_WIDTH + WorldToolsPanel.FRAME_MARGIN*2, WorldToolsPanel.TOOLS_HEIGHT + WorldToolsPanel.FRAME_MARGIN*2)
        self.setFrameRect(QRect(0, 0, WorldToolsPanel.TOOLS_WIDTH + WorldToolsPanel.FRAME_MARGIN*2, WorldToolsPanel.TOOLS_HEIGHT + WorldToolsPanel.FRAME_MARGIN*2))        
        
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
                        
        self.create_stickman = QPushButton('Create Stickman', self)
        self.create_stickman.resize(WorldToolsPanel.BUTTON_WIDTH, WorldToolsPanel.TOOLS_HEIGHT)
        self.create_stickman.move(WorldToolsPanel.FRAME_WIDTH*2, WorldToolsPanel.FRAME_MARGIN)        
        self.create_stickman.setStyleSheet(button_stylesheet)
        self.create_stickman.clicked.connect(self.showCreateDialog)
        
        self.create_stickman_input = InputLine(self)
        self.create_stickman_input.setLabelText("Enter New StickName: ")
        self.create_stickman_input.addOkListener(self.readCreateName)
        self.create_stickman_input.addCancelListener(self.hideCreateDialog)
        self.create_stickman_input.move(WorldToolsPanel.FRAME_MARGIN, WorldToolsPanel.FRAME_MARGIN)
        self.create_stickman_input.hide()
        
        self.delete_stickman = QPushButton('Delete Stickman', self)
        self.delete_stickman.resize(WorldToolsPanel.BUTTON_WIDTH, WorldToolsPanel.TOOLS_HEIGHT)
        self.delete_stickman.move(WorldToolsPanel.BUTTON_WIDTH + WorldToolsPanel.FRAME_MARGIN, WorldToolsPanel.FRAME_MARGIN)        
        self.delete_stickman.setStyleSheet(button_stylesheet)
        self.delete_stickman.clicked.connect(self.showDeleteDialog)
        
        self.delete_stickman_input = InputLine(self)
        self.delete_stickman_input.setLabelText("Enter Name to Delete: ")
        self.delete_stickman_input.addOkListener(self.readDeleteName)
        self.delete_stickman_input.addCancelListener(self.hideDeleteDialog)
        self.delete_stickman_input.move(WorldToolsPanel.FRAME_MARGIN, WorldToolsPanel.FRAME_MARGIN)
        self.delete_stickman_input.hide()
        
        self.change_background = QPushButton('Set Background', self)
        self.change_background.resize(WorldToolsPanel.BUTTON_WIDTH, WorldToolsPanel.TOOLS_HEIGHT)
        self.change_background.move(WorldToolsPanel.BUTTON_WIDTH*2 + WorldToolsPanel.FRAME_MARGIN, WorldToolsPanel.FRAME_MARGIN)        
        self.change_background.setStyleSheet(button_stylesheet)
        self.change_background.clicked.connect(self.findBackground)
        
        self.remove_background = QPushButton('Clear Background', self)
        self.remove_background.resize(WorldToolsPanel.BUTTON_WIDTH, WorldToolsPanel.TOOLS_HEIGHT)
        self.remove_background.move(WorldToolsPanel.BUTTON_WIDTH*3 + WorldToolsPanel.FRAME_MARGIN, WorldToolsPanel.FRAME_MARGIN)        
        self.remove_background.setStyleSheet(button_stylesheet)       
        self.remove_background.clicked.connect(self.clearBackground)
        
    """ Methods which show and hide input lines and buttons. ALso methods for resizing the panel and its frame """
    def showCreateDialog(self):
        self.resizeForInput()
        self.hideButtons()  
        self.create_stickman_input.setText("")
        self.create_stickman_input.setErrorText("")
        self.create_stickman_input.show() 
    def hideCreateDialog(self):        
        self.resizeForButtons()
        self.create_stickman_input.hide()  
        self.showButtons()
        
    def showDeleteDialog(self):
        self.resizeForInput()
        self.hideButtons()
        self.delete_stickman_input.setText("")
        self.delete_stickman_input.setErrorText("")
        self.delete_stickman_input.show() 
    def hideDeleteDialog(self):
        self.resizeForButtons()
        self.delete_stickman_input.hide()  
        self.showButtons()
        
    def hideButtons(self):
        self.create_stickman.hide()
        self.delete_stickman.hide()
        self.change_background.hide()
        self.remove_background.hide()       
    def showButtons(self):
        self.create_stickman.show()
        self.delete_stickman.show()
        self.change_background.show()
        self.remove_background.show()
    
    def resizeForButtons(self):
        self.resize(WorldToolsPanel.TOOLS_WIDTH + WorldToolsPanel.FRAME_MARGIN*2, WorldToolsPanel.TOOLS_HEIGHT + WorldToolsPanel.FRAME_MARGIN*2)
        self.setFrameRect(QRect(0, 0, WorldToolsPanel.TOOLS_WIDTH + WorldToolsPanel.FRAME_MARGIN*2, WorldToolsPanel.TOOLS_HEIGHT + WorldToolsPanel.FRAME_MARGIN*2))  
    def resizeForInput(self):    
        self.resize(WorldToolsPanel.INPUT_WIDTH + WorldToolsPanel.FRAME_MARGIN*2 + InputLine.ERROR_WIDTH, WorldToolsPanel.TOOLS_HEIGHT + WorldToolsPanel.FRAME_MARGIN*2)
        self.setFrameRect(QRect(0, 0, WorldToolsPanel.INPUT_WIDTH + WorldToolsPanel.FRAME_MARGIN*2, WorldToolsPanel.TOOLS_HEIGHT + WorldToolsPanel.FRAME_MARGIN*2))   
    
    """ listener for the file dialog method to open the file for the background"""
    def findBackground(self):
        file = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files (*.png *.jpg)")
        if file[0] != "":
            getWorld().setBackground(file[0])
    def clearBackground(self):
        getWorld().clearBackground("#FFFFFF")
           
    """ Listeners to take actions when ok button was pressed and input text has been read """
    def readCreateName(self):
        if self.create_stickman_input.getText() == "":
            self.create_stickman_input.setErrorText("StickName cannot be empty!")
        elif getWorld().exists(self.create_stickman_input.getText()):
            self.create_stickman_input.setErrorText("This StickName is already taken!")
            self.create_stickman_input.setText("")
        elif len(self.create_stickman_input.getText()) >  WorldToolsPanel.STICKMAN_NAME_MAX_LENGTH:
            self.create_stickman_input.setErrorText("StickName is too long!")
            self.create_stickman_input.setText("")
        else:
            getWorld().createStickman(self.create_stickman_input.getText(), WorldToolsPanel.STICKMAN_X, WorldToolsPanel.STICKMAN_Y)
            self.hideCreateDialog()
                   
    def readDeleteName(self):
        if self.delete_stickman_input.getText() == "":
            self.delete_stickman_input.setErrorText("StickName cannot be empty!")
        elif not getWorld().exists(self.delete_stickman_input.getText()):
            self.delete_stickman_input.setErrorText("This StickName does not exist!")
            self.delete_stickman_input.setText("")
        else:
            getWorld().removeStickman(self.delete_stickman_input.getText())
            self.hideDeleteDialog()

