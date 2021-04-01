import sys
import threading
from os.path import abspath
from os import system
from math import floor, ceil
from time import sleep
from itertools import zip_longest

import pygame
from pygame.display import init
from pygame.locals import *
from grid import Grid
from pygame_textinput import TextInput

if system("python -m pip install pygame-button") != 0:
    print(
"""ERROR: tried to install pygame-button module via

python -m pip install pygame-button

This module is necessary for the program to run
Please check your internet connection and try again, or run the command yourself"""
)
    input("Press enter to exit...")
    sys.exit()

from pygame_button import Button
pygame.init()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BG = WHITE
FG = BLACK

CLOCK = pygame.time.Clock()
FPS = 30

SCREEN = pygame.display.set_mode((100, 100), FULLSCREEN)
pygame.display.set_caption("Animated addition")
font_obj = pygame.font.Font("calibri.ttf", 24)

"""-------------------------------------------------Define Functions"""
delay = 1 #Delay between animation steps

def clear_and_draw_baseline():
    "Draw the base line and operator" 
    grid.clear(BG)
    for i in range(grid.x_blocks):
        grid.draw("H", i, bottom_line)
    
    grid.draw("+", 0, bottom_line - 1)

force_stop = False
def addition_manager():
    global force_stop
    
    force_stop = True
    sleep(0.06)
    force_stop = False

    for i in addition():
        for j in range(int(delay / 0.05)):
            sleep(0.05)
            if force_stop:
                return()

def addition():
    "The part that actually adds"
    clear_and_draw_baseline()

    top_num = int(top_input.get_text().strip())
    bottom_num = int(bottom_input.get_text().strip())
    top_num, bottom_num = sorted( #Longest number on top
        (top_num, bottom_num),
        key=(lambda x: len(str(x))),
        reverse=True        
    )

    sum_string = str(top_num + bottom_num)
    top_list = list(str(top_num))
    bottom_list = list(str(bottom_num))
    
    #The animation runs right to left, so the lists are reversed
    top_list.reverse()
    bottom_list.reverse()
    right_side = grid.x_blocks - 1

    #bottom_line is the sum line
    #bottom_line - 1 is the bottom addend
    #bottom_line - 2 is the top addend
    #bottom_line - 3 is the carry row

    #Draw the numbers then wait
    grid.draw(str(bottom_num), right_side, bottom_line - 1)
    grid.draw(str(top_num), right_side, bottom_line - 2)
    pygame.display.flip(); yield
    
    move = 0
    carry_sum = 0
    for (top, bottom) in zip_longest(top_list, bottom_list, fillvalue="0"):
        r_sum = int(top) + int(bottom) + carry_sum #Add column
        if r_sum > 9: #If there's a carry

            #Draw the ones part
            grid.draw(r_sum - 10, right_side - move, bottom_line)
            pygame.display.update(); yield

            #Draw the carry digit
            carry_sum = 1
            grid.draw("1b", right_side - move - 1, bottom_line - 3)
                    
        else: #If there's no carry

            #Draw the sum as normal
            grid.draw(r_sum, right_side - move, bottom_line)
            carry_sum = 0

        pygame.display.update(); yield True
        move += 1
    
    #If there's a carry digit left, draw it on the bottom line
    if carry_sum == 1:
        grid.draw(1, right_side - move, bottom_line)
    
    pygame.display.update(); yield

    #Highlight the sum green once the animation is complete
    n = 0
    for x in range(right_side - len(sum_string), right_side):
        grid.draw(sum_string[n] + "r", x + 1, bottom_line)
        n += 1
    
    yield

"""-----------------------------------------------------Define input"""
if True: #I'm sick of seeing these blocks of code. if True does the job
    top_input = TextInput(
        font_family=abspath("calibri.ttf"), 
        max_string_length=10, 
        initial_string="23",
        cursor_color=BG
        )
    top_input.update(pygame.event.get())

    bottom_input = TextInput(
        font_family=abspath("calibri.ttf"),
        max_string_length=10,
        initial_string="79",
        cursor_color=BG
    )
    bottom_input.update(pygame.event.get())
    focus = "" #Empty is no focus

"""--------------------------------------------------Define the grid"""
if True:
    SCREEN.fill(BG)
            
    WIDTH = SCREEN.get_width()
    HEIGHT = SCREEN.get_height()

    divider = ceil(0.7 * WIDTH)

    #making_grid.md for explanation
    rect_height = floor(divider * 4/3)
    if rect_height > HEIGHT:
        rect_width = HEIGHT * 3/4
        rect_height = HEIGHT
    else:
        rect_width = divider

    #Change the eights to any power of 2 to change the size. 
    #8 is perfect though
    grid_width = int(divider // (rect_width // 8))
    grid_height = int(HEIGHT // (rect_height // 8))

    grid = Grid(SCREEN, divider, HEIGHT, grid_width, grid_height, FG, 1)
    grid.update()

    #------Make the divider line
    #The right edge of the grid, adjusted to match the difference of 
    # the grid and ceil(0.7 * WIDTH) Added 40 pixels of margin. 20 left side, 20 right side
    divider = divider // grid_width * grid_width + 40

    pygame.draw.line(
        SCREEN, 
        RED,
        (divider, 0),
        (divider, HEIGHT),
        grid.thickness * 2 + 1
    )

    #Line beneath numbers. Right side.
    Z = HEIGHT // 4 #Fuckit im calling Z.
    pygame.draw.line(
        SCREEN,
        BLACK,
        (divider, Z),
        (WIDTH, Z),
        2
    )
    bottom_line = grid.y_blocks - 2
    clear_and_draw_baseline()

"""-------------------------------Input box coords and define button"""
if True:
    padding = 10
    top_coords = [divider + padding, 10]
    bottom_coords = [divider + padding, Z / 4 + 10]

    button_width = WIDTH - divider - 2 * padding
    button_height = Z - ceil(0.6 * Z) - padding
    addition_button = Button(
        (divider + padding, ceil(0.6 * Z), button_width, button_height),
        BLUE, 
        (lambda: threading.Thread(target=addition_manager, daemon=True).start()), 
        text="+",
        **{"font": font_obj, "hover_color": (0, 0, 127)}
    )

while True:
      
    """------Event loop"""
    events = pygame.event.get()
    for event in events:
        #Fill just the button area, don't redraw everything if you don't have to
        SCREEN.fill(WHITE, (divider + padding, 0, WIDTH, Z))

        keys = pygame.key.get_pressed()
        if event.type == QUIT or keys[K_ESCAPE]: 
            pygame.quit()
            sys.exit()
        
        """Focus on the box and fix the cursor color"""
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #It stores the surface, not the rect, so this ugly thing is used to get one
            t_rect = top_input.get_surface().get_rect().move(*top_coords)
            b_rect = bottom_input.get_surface().get_rect().move(*bottom_coords)

            if t_rect.collidepoint(pos):
                focus = "top"
                top_input.set_cursor_color(FG)
                bottom_input.set_cursor_color(FG)

            elif b_rect.collidepoint(pos):
                focus = "bottom"
                top_input.set_cursor_color(FG)
                bottom_input.set_cursor_color(FG)

            else:
                focus = ""
                top_input.set_cursor_color(BG)
                top_input.update(events)
                bottom_input.set_cursor_color(BG)
                bottom_input.update(events)
        
        addition_button.check_event(event)
    
    addition_button.update(SCREEN)

    """Input handling outside loop"""  
    if focus == "top":
        top_input.update(events)
    
    elif focus == "bottom":
        bottom_input.update(events)
    
    #If the string is empty, put a space. 
    #Otherwise the surface will be 1x1 and can't be clicked on again

    for boxy_boi in (top_input, bottom_input):
        if len(boxy_boi.input_string) == 0: 
            boxy_boi.input_string = "   "
    
    SCREEN.blit(top_input.get_surface(), top_coords)
    SCREEN.blit(bottom_input.get_surface(), bottom_coords)
    
    pygame.draw.rect(SCREEN, BLACK, (
        (top_coords[0] - 5, top_coords[1] - 5), 
        (top_input.get_surface().get_size()[0] + 10, top_input.get_surface().get_size()[1] + 10)
    ), 2)

    pygame.draw.rect(SCREEN, BLACK, (
        (bottom_coords[0] - 5, bottom_coords[1] - 5), 
        (bottom_input.get_surface().get_size()[0] + 10, bottom_input.get_surface().get_size()[1] + 10)
    ), 2)

    pygame.display.flip()
    CLOCK.tick(FPS)
