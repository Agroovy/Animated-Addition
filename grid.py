#Class for a simple grid
from math import ceil, floor

import pygame
from pygame.locals import *
pygame.init()

#A big font is made, then scaled to the size of the squares
FONT = pygame.font.Font("calibri.ttf", 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (255, 255, 255)
FG = (0, 0, 0)

"""Define the surfaces of the numbers"""
text_dict = {}

#Operators, numbers, numbers with decimal point (1., 0)
loop_list_1 = ["+", "-", "*", "=", ".", " "]\
+ list(range(0, 10))\
+ [str(i) + "." for i in range(0,10)]\

#To access a number, use ["0"] instead of [0]
for i in loop_list_1: 
    text_dict[str(i)] = FONT.render(str(i), True, FG)

"---COLORS"
for j in [str(i) + "r" for i in range(0,10)]:
    text_dict[j] = FONT.render(j[0], True, RED)

for j in [str(i) + "g" for i in range(0,10)]:
    text_dict[j] = FONT.render(j[0], True, GREEN)

for j in [str(i) + "b" for i in range(0,10)]:
    text_dict[j] = FONT.render(j[0], True, BLUE)

"""Horizontal bar"""
w, h = text_dict["0"].get_size()
h_line = pygame.Surface((w, h))
h_line.fill(BG)
pygame.draw.line(h_line, FG, (0, 1), (w, 1), 5)

text_dict["H"] = h_line


class Grid():
    def __getitem__(self, index):
        return(self.grid[index])
    
    def __init__(self, screen, x_pixels, y_pixels, x_blocks, y_blocks, color=(0, 0, 0), thickness=1):
        self.color = color
        self.thickness = thickness
        self.screen = screen
        self.x_pixels = x_pixels
        self.y_pixels = y_pixels
        self._set_grid(x_pixels, y_pixels, x_blocks, y_blocks)
        
    
    def _set_grid(self, width, height, x_blocks, y_blocks):
        
        """Create the grid to be drawn on.
        The elements of the grid are accessed like my_obj.grid[x_coord][y_coord]
        Each element is a rect."""

        self.width = width
        self.height = height
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        self.unit_width = width // x_blocks #x pixels per block
        self.unit_height = height // y_blocks #y pixels per block

        total_grid = []
        for x in range(x_blocks):
            column = []
            for block in range(y_blocks):
                column.append(
                    pygame.Rect(
                        self.unit_width * x + 20, #10 pixels of margin
                        self.unit_height * block,
                        self.unit_width,
                        self.unit_height
                    )
                )
            total_grid.append(column)
        self.grid = total_grid

    def update(self):
        """Draw the entire grid to a surface"""
        for column in self.grid:
            for element in column:
                pygame.draw.rect(self.screen, self.color, element, self.thickness)
    
    def draw(self, text, x=0, y=0):
        """Draws a number/letter to the specified grid square. x and y are the rightmost digit if the number. It's drawn right to left"""
        
        text = str(text) #Allow numbers to be passed through

        #This groups letters or decimal points to numbers
        #putting in "467.2" makes a list of ['4','6','7.',2]
        #[1r2.3] gives ['1r','2.','3']
        #This makes drawing it easier since they're dictionary keys
        char_list = []
        i = 0
        while i < len(text):
            if i < len(text) - 1 and text[i+1] in (".", "r", "g", "b"):
                char_list.append(text[i] + text[i+1])
                i += 2
            else:
                char_list.append(text[i])
                i += 1
        char_list.reverse()
        
        counter = 0
        wrap = 0
        for char in char_list:
            if counter == len(char_list):
                #Wrap the numbers to the next line
                wrap += 1
                counter = 0
            
            #Scale down
            surf = pygame.transform.scale(
                text_dict[char], 
                (self.unit_width, self.unit_height)
            )
            
            self.screen.blit(
                surf, 
                (
                    self[x - counter][y + wrap].x, 
                    self[x - counter][y + wrap].y
                )
            )
            counter += 1
    
    def clear(self, fill_color):
        """Clear the entire grid by drawing over it. The internal data is unchanged"""
        self.screen.fill(fill_color,
            pygame.Rect(self.grid[0][0].topleft,
                (self.x_pixels, self.y_pixels)
            )
        )

