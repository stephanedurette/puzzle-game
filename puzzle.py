import cv2
import numpy as np
from puzzlePiece import puzzle_piece as piece
import random

class puzzle():
    def __init__(self,ogImage,size = 3, scale = .5,borderPixels = 2):
        self.borderPixels = borderPixels
        self.size = size
        self.pieces = []
        self.scale = scale
        self.ogImage = ogImage
        self.isSolved = False
        
        self.initializePuzzle()
        #self.show_image(self.borderPixels)
    
    def mouse_click(self,event,x,y,flags,param):
        if self.isSolved:
            return
        if event == cv2.EVENT_LBUTTONDOWN:
            index = self.get_clicked_tile_index(x, y)
            neighbors = self.get_adjacent_indeces(index)
            print('index:', index)
            print('neighbors', neighbors)
            for i in range(len(neighbors)):
                if self.pieces[neighbors[i]].get_isBlackedOut():
                    self.swap_pieces(index, neighbors[i])
                    if self.is_solved():
                        self.handle_solved()
                    return
    
    def update(self, image):
        self.ogImage = image
        self.resizeImage()
        self.update_pieces()
        if self.isSolved:
            self.show_image(1)
        else:
            self.show_image(self.borderPixels)
        
    
    def handle_solved(self):
        for p in self.pieces:
            if p.get_isBlackedOut():
                p.set_blackout(False)
        self.isSolved = True
    
    def get_clicked_tile_index(self, x, y):
        
        
        xInd = x // (self.wSize + 2 * self.borderPixels)
        yInd = y // (self.hSize + 2 * self.borderPixels)
        return yInd * self.size + xInd
        
    def get_adjacent_indeces(self, index):
        indeces = []
        if(index + self.size >= 0 and index + self.size < len(self.pieces)):
            indeces.append(index + self.size)  
        if(index - self.size >= 0 and index - self.size < len(self.pieces)):
            indeces.append(index - self.size)   
        if (not((index + 1) % self.size) == 0):
            indeces.append(index + 1)
        if (not(index % self.size == 0)):
            indeces.append(index - 1)
        return indeces
    
    def initializePuzzle(self):
        self.resizeImage()
        self.height, self.width = self.ogImage.shape[:2]
    
        #get segment size
        self.wSize = self.width // self.size
        self.hSize = self.height // self.size
        
        self.init_pieces()
        self.shuffle_puzzle()
        
        cv2.namedWindow('puzzle')
        cv2.setMouseCallback('puzzle',self.mouse_click)
        
    def is_solved(self):
        for i in range(len(self.pieces)):
            if i != self.pieces[i].get_startIndex():
                return False
        return True
    
    def update_pieces(self):
        
        images = [0] * self.size**2
        index = 0
        for i in range(0, self.size):
            h_start = i * self.hSize
            for j in range(0, self.size):
                w_start = j * self.wSize
                segment = self.ogImage[h_start:h_start + self.hSize,w_start:w_start + self.wSize]
                images[index] = segment
                index += 1
        for i in range(len(self.pieces)):
            pieceIndex = self.pieces[i].get_startIndex()
            self.pieces[i].update(images[pieceIndex])
    
    def init_pieces(self):
        index = 0
        for i in range(0, self.size):
            h_start = i * self.hSize
            for j in range(0, self.size):
                w_start = j * self.wSize
                segment = self.ogImage[h_start:h_start + self.hSize,w_start:w_start + self.wSize]
                self.pieces.append(piece(index, segment))
                index += 1
        self.pieces[len(self.pieces) - 1].set_blackout(True)
    
    def resizeImage(self):
        self.ogImage = cv2.resize(self.ogImage,None,fx=self.scale, fy=self.scale, interpolation = cv2.INTER_CUBIC)
        
        height, width = self.ogImage.shape[:2]
        self.ogImage = cv2.resize(self.ogImage,(width - (width % self.size), height - (height % self.size)))
        
        
    def show_image(self, borderPixels):
        concats = []
        temp = []
        for i in range(len(self.pieces)):
            if ((i != 0) and (i % self.size == 0)):
                concats.append(chain_concat(temp, 1))
                temp = []
            temp.append(self.pieces[i].get_image(borderPixels))
        concats.append(chain_concat(temp, 1))
        
        img = chain_concat(concats, 0)
        if (self.isSolved):
            cv2.putText(img,'You Win!!!', (int(self.width / 2) - 250 ,int(self.height / 2) - 50), cv2.FONT_HERSHEY_SIMPLEX, 4,(0,0,0),4)
        cv2.imshow('puzzle', img)
            
    def shuffle_puzzle(self):
        length = len(self.pieces)
        for i in range(length - 1):
            randIndex = random.randint(i + 1, length - 1)
            self.swap_pieces(i, randIndex)
            
        if(not self.is_solvable()):
            if(self.pieces[0].isBlackedOut or self.pieces[1].isBlackedOut):
                self.swap_pieces(len(self.pieces) - 1, len(self.pieces) - 2)
            else:
                self.swap_pieces(0, 1)

    def swap_pieces(self, index_1, index_2):
        temp = self.pieces[index_1]
        self.pieces[index_1] = self.pieces[index_2]
        self.pieces[index_2] = temp
        
        self.pieces[index_1].set_index(index_1)
        self.pieces[index_2].set_index(index_2)
        
    def count_inversions(self, index):
        inversionCount = 0
        i_val = self.pieces[index].get_startIndex()
        for i in range(index, len(self.pieces)):
            val = self.pieces[i].get_startIndex()
            if val < i_val:
                inversionCount += 1
        return inversionCount
    
    def is_solvable(self):
        if self.size % 2 == 1:
            return (self.sum_inversions() % 2) == 0
        else:
            return ((self.sum_inversions() + self.size - self.get_empty_row()) % 2) == 0
        
    def sum_inversions(self):
        inversion_count = 0
        for i in range(len(self.pieces)):
            if(self.pieces[i].get_isBlackedOut() == False):
                inversion_count += self.count_inversions(i)
        return inversion_count 
    
    def get_empty_row(self):
        index = -1
        for i in range(len(self.pieces)):
            if(self.pieces[i].get_isBlackedOut()):
                index = i
        return index // self.size + 1
                
            
        
def chain_concat(imageArray, axis):
    img = imageArray[0]
    for i in range(1, len(imageArray)):
        img = np.concatenate((img, imageArray[i]), axis = axis)
    return img

        
        
        
        