'''
Created on May 13, 2015

@author: Artem
'''

from PyQt5.Qt import QIcon, QPixmap

class AssetLoader():
    
    def initialize(self):        
        self.camera = QIcon("resources/camera.png")
        self.confused = QIcon("resources/confused.png")
        self.copy = QIcon("resources/copy.png")
        self.delete = QIcon("resources/delete.png")
        self.down = QIcon("resources/down.png")
        self.enter = QIcon("resources/enter.png")
        self.exit = QIcon("resources/exit.png")
        self.pause = QIcon("resources/pause.png")
        self.play = QIcon("resources/play.png")
        self.sad = QIcon("resources/sad.png")
        self.say_left = QIcon("resources/say_left.png")
        self.say_right = QIcon("resources/say_right.png")
        self.smile = QIcon("resources/smile.png")
        self.speak_left = QPixmap("resources/speak_left.png")
        self.speak_right = QPixmap("resources/speak_right.png")
        self.stickman = QIcon("resources/stickman.png")
        self.stop = QIcon("resources/stop.png")
        self.time = QIcon("resources/time.png")
        self.up = QIcon("resources/up.png")        
        
assets = AssetLoader()