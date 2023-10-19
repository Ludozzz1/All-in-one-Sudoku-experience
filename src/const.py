import pygame as pg
from error import *

#All constants and global variables used in the program are defined here.

width, height = 1920, 1080
novalue = -1
sudoku_size = 9
off_x = 700
off_y = 250
box_size = 504
dif = box_size // sudoku_size
x = 0
y = 0
inserting_x, inserting_y = None, None
start = False
special_mode = False
solved = False
note = False
user_input_rect = pg.Rect(800, 800, 230, 50)
input_x, input_y = 800, 800
input_width, input_height = 230, 50
input_padding = 5
number_padding_x = 19
number_padding_y = 15
special_number_padding_x = 5
special_number_padding_y = 4
max_char = 100
max_input_width = 10
num_input = ""
error = InsertionError("", 0)
message_x = 950
message_y = 175
coord_x = 1510
coord_y = 350
error_x = 1510
error_y = 425
finish_x = 1510
finish_y = 500
start_button_border = 5
end_button_border = 10
button_width, button_height = 200, 50
start_button_x, start_button_y = 300, 250
solve_button_x, solve_button_y = 300, 700
cancel_button_x, cancel_button_y = 1410, 250    
start_again_x = 860
start_again_y = 825
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
dark_green = (0, 100, 0)
button_color = (0, 128, 0)
blue = (0, 0, 255)