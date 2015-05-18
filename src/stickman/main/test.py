'''
Created on May 02, 2015

@author: Artem
'''

import unittest
import random
import string

from stickman.model.World import getWorld
from stickman.tools.XMLAdapter import XML

import xml.etree.ElementTree as ET

class Test(unittest.TestCase):

    """ Basic World functionality tests """  
    def testStickmanCreation(self):
        
        for _ in range(0, 20):
            x = random.randint(200, 500)
            y = random.randint(100, 300)
            
            name = ""
            for _ in range(0, 7): 
                name += random.choice(string.ascii_letters)
                        
            getWorld().createStickman(name, x, y)            
            stickman = getWorld().getActive()
            self.assertEqual(name, stickman.name, "Stickman was not created correctly!")
        
        self.assertEqual(len(getWorld().stickmen), 20, "There are less stickmen created than expected!")
                        
    def testStickmanDelition(self):
        
        for i in range(0, 10):                              
            stickman = getWorld().getActive()
            getWorld().removeStickman(stickman.name)
            self.assertEqual(len(getWorld().stickmen), 20-i-1, "Stickman was not properly removed!")
        
        getWorld().removeStickman("This name does not exist!")
        self.assertEqual(len(getWorld().stickmen), 10, "non-existent stickman removed!")
    
    """ utility functions test """
    def test_xml(self):        
        #test the stickman to xml conversion
        for stickman in getWorld().stickmen:
            root = ET.Element("stickman")                             
            XML().stickmanToXML(stickman, root)
            self.assertTrue(str(ET.tostring(root, encoding="utf-8")).startswith("b'<stickman><name>" + stickman.name + "</name><x>" + 
                                                                                str(stickman.x) + "</x><y>" + str(stickman.y) + "</y>"), 
                            "Stickman XML is not valid!")
        
        #test whole animation conversion
        frames = list()
        for i in range(0, 10):
            frame = getWorld().getFrame()
            frame.time = i+1
            frames.append(frame)
            
        XML().toXML(frames, "test.armo")
        frames = XML().fromXML("test.armo")
        
        for i in range(0, 10):
            self.assertEqual(frames[i].time, i+1, "Loaded frame time is incorrect!")
            self.assertTrue(len(frames[i].stickmen) == 10, "Stickmen were incorrectly loaded!")
    
    """ movement tests """
    def test_movements(self):
        #test body movements
        stickman = getWorld().getActive()
        coor = (stickman.x, stickman.y)
        
        stickman.moveTo(-200, -300)
        self.assertEqual(coor, (stickman.x, stickman.y), "Stickman should not move over the bounds of the field!")
        
        # test mouse moving stickman body
        for _ in range(0, 10):
            new_x = random.randint(100, 500)
            new_y = random.randint(200, 400)
            coor = (stickman.x, stickman.y)
            getWorld().mousePressed(coor[0], coor[1])
            getWorld().mouseMoved(new_x, new_y)
            getWorld().mouseReleased(new_x, new_y)
            self.assertEqual((stickman.x, stickman.y), (new_x, new_y), "Stickman was not dragged to the proper location!")
        
        left_elbow = stickman.joints[9]
        self.assertTrue(left_elbow.isActive, "The elbow should be an active joint!")
             
        for _ in range(0, 10):
            relative_x = left_elbow.x
            relative_y = left_elbow.y
            x = relative_x + stickman.x
            y = relative_y + stickman.y
        
            getWorld().mousePressed(x, y)
            self.assertTrue(left_elbow.dragged, "Left elbow should be dragged!")
           
if __name__ == "__main__":
    unittest.main()
    

