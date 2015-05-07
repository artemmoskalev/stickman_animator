'''
Created on Apr 26, 2015

@author: Artem
'''

from stickman.tools.WorldTools import StickmanTools
from stickman.tools.AnimationTools import AnimationTools
from stickman.tools.IOTools import IOTools

"""
    ---------------------------------------

    class which holds the references to the tool sets in order to switch them. can define their position and hide/show the tools
    
    ---------------------------------------

"""
class ToolSet():
    
    def __init__(self, parent):
        self.stickman_tools = StickmanTools(parent)
        self.animation_tools = AnimationTools(parent)
        self.io_tools = IOTools(parent)
        self.hide()
        
    def move(self, x, y):
        self.stickman_tools.move(x, y)
        self.animation_tools.move(x, y)
        self.io_tools.move(x, y)
                
    def showStickmanTools(self):        
        self.hide()        
        self.stickman_tools.show()
        self.stickman_tools.showButtons()
        
    def showAnimationTools(self):
        self.hide()
        self.animation_tools.show()
        
    def showIOTools(self):
        self.hide()
        self.io_tools.show()   
        
    def hide(self):
        self.stickman_tools.hide()
        self.animation_tools.hide()
        self.io_tools.hide()
        
