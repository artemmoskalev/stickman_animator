'''
Created on May 14, 2015

@author: Artem
'''

import xml.etree.ElementTree as ET

from stickman.tools.Components import Frame
from stickman.model.World import Stickman, Joint

class XML():
    
    """ Methods for streaming frames into XML """
    def toXML(self, frame_list, file):
        root = ET.Element("animation")     
        #process all frames one by one   
        for frame in frame_list:        
            frame_root = ET.SubElement(root, "frame")    
            self.frameToXML(frame, frame_root)
        #save the DOM tree into the file
        ET.ElementTree(root).write(file)
        
    def frameToXML(self, frame, root):        
        time_element = ET.SubElement(root, "time")
        time_element.text = str(frame.time)    
        #process stickmen one by one
        for stickman in frame.stickmen:
            stickman_root = ET.SubElement(root, "stickman")
            self.stickmanToXML(stickman, stickman_root)
    
    def stickmanToXML(self, stickman, root):
        name_element = ET.SubElement(root, "name")
        name_element.text = stickman.name
        x_element = ET.SubElement(root, "x")
        x_element.text = str(stickman.x)
        y_element = ET.SubElement(root, "y")
        y_element.text = str(stickman.y)
        expression_element = ET.SubElement(root, "expression")
        expression_element.text = str(stickman.head.expression.expression)
        
        words_element = ET.SubElement(root, "words")
        text_element = ET.SubElement(words_element, "text")
        text_element.text = stickman.words.text
        side_element = ET.SubElement(words_element, "side")
        side_element.text = str(stickman.words.side)
        
        for joint in stickman.joints:
            #process joints one by one
            joint_root = ET.SubElement(root, "joint")
            self.jointToXML(joint, stickman.joints, joint_root)
        
    def jointToXML(self, joint, joint_list, root):
        is_active_element = ET.SubElement(root, "active")
        is_active_element.text = str(joint.isActive)
        x_element = ET.SubElement(root, "x")
        x_element.text = str(joint.x)
        y_element = ET.SubElement(root, "y")
        y_element.text = str(joint.y)
        
        #find the next joint. If it exists, find it in the list of joints and write down its index
        next_element = ET.SubElement(root, "next")
        if joint.next == None:
            next_element.text = "None"
        else:
            next_element.text = str(joint_list.index(joint.next))
        
        #find the previous joint, and if it exists, write down its index and accompanying information
        attachment_element = ET.SubElement(root, "attachment")
        if joint.attachment == None:
            attachment_element.text = "None"
        else:
            attachment_element.text = str(joint_list.index(joint.attachment))
            
            angle_element = ET.SubElement(root, "angle")
            angle_element.text = str(joint.angle)            
            length_element = ET.SubElement(root, "length")
            length_element.text = str(joint.length)        
        
    
    """ methods for creating frames from XML """
    def fromXML(self, xml, file):
        tree = ET.parse(file)
        animation = tree.getroot()
        
        frames = list()
        for frame_element in animation:
            frames.append(self.decodeFrame(frame_element)) 
    
        return frames
    
    def decodeFrame(self, root):
        frame = Frame(int(root.find("time").text))
        
        stickmen = list()
        for stickman_element in root.iter("stickman"):
            stickmen.append(self.decodeStickman(stickman_element))
        
        frame.stickmen = stickmen        
        return frame
    
    def decodeStickman(self, root):
        name = root.find("name").text
        x = int(root.find("x").text)
        y = int(root.find("y").text)
        
        stickman = Stickman(name, x, y)
        
        stickman.head.expression.expression = int(root.find("expression").text)   
        stickman.words.text = root.find("words").find("text").text
        if stickman.words.text == None:
            stickman.words.text = ""
        stickman.words.side = int(root.find("words").find("side").text)
        
        joints = list()
        #iterate for the first time to fill in the list with joints in the correct order
        for joint_element in root.iter("joint"):            
            if joint_element.find("active").text == "True":
                joint_isActive = True
            else:
                joint_isActive = False
            joint_x = float(joint_element.find("x").text)
            joint_y = float(joint_element.find("y").text)
            
            joint = Joint(stickman, joint_isActive, joint_x, joint_y)
            
            if joint_element.find("next").text == "None":
                joint.next = None
            else:
                joint.next = int(joint_element.find("next").text)
            
            if joint_element.find("attachment").text == "None":
                joint.attachment = None
                joint.angle = None
                joint.length = None
            else:
                joint.attachment = int(joint_element.find("attachment").text)
                joint.angle = float(joint_element.find("angle").text)
                joint.length = float(joint_element.find("length").text)
            
            joints.append(joint)
        
        #iterate through the list of joints once mroe to restore the relationships between joints
        for joint in joints:
            if joint.next != None:
                joint.next = joints[joint.next]
            if joint.attachment != None:
                joint.attachment = joints[joint.attachment]
        
        stickman.joints = joints
        return stickman
            
    