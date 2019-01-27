import numpy as np
import cv2

class puzzle_piece():
    def __init__(self, startIndex, pictureImage, isBlackedOut = False):
        self.index = startIndex
        self.emptyColor = [0,0,0]
        self.pictureImage = pictureImage
        self.image = np.copy(self.pictureImage)
        self.startIndex = startIndex
        self.isBlackedOut = isBlackedOut
        self.blackedOutImage = np.copy(self.pictureImage)
        self.blackedOutImage[:] = self.emptyColor
    
    def get_isBlackedOut(self):
        return self.isBlackedOut
    
    def get_image(self, border):
        return cv2.copyMakeBorder(self.image,border,border,border,border,cv2.BORDER_CONSTANT,value=self.emptyColor)
    
    def update(self, image):
        if(self.isBlackedOut == False):
            self.image = image
        
    def get_index(self):
        return self.index
    
    def set_index(self, index):
        self.index = index
    
    def set_normal_image(self):
        self.image = np.copy(self.pictureImage)
    
    def set_image(self, image):
        self.image = image
        
    def set_blackout(self, val):
        self.isBlackedOut = val
        if val:
            self.image = self.blackedOutImage
        
    def copy(self):
        return puzzle_piece(self.startIndex, self.image, self.isBlackedOut)
    
    def get_startIndex(self):
        return self.startIndex

