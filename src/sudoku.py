import numpy as np
import pygame as pg
import sys
from const import *
from error import *

#aggiungere note

pg.init()

font = pg.font.SysFont("calibri", 30)
number_font = pg.font.SysFont("calibri", 40)
special_num_font = pg.font.SysFont("calibri", 25)
pg.display.set_caption("Sudoku Solver")
screen = pg.display.set_mode((width, height))
screen.fill(white)
sudoku = np.full((sudoku_size, sudoku_size), novalue)
is_special = np.full((sudoku_size, sudoku_size), False)
is_inserted = np.full((sudoku_size, sudoku_size), False)
 
# Function to solve sudoku with backtracking. 
# It uses the check_costraints function to check if the number is valid.
# It takes the sudoku as grid, and the row and the column in which you want to try to insert the numbers.

def resolve_sudoku(grid, row, col):
    if (row == sudoku_size - 1 and col == sudoku_size):
        return True
    if col == sudoku_size:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return resolve_sudoku(grid, row, col + 1)
    for num in range(1, sudoku_size + 1, 1):
        if check_costraints(col, row, num):
            grid[row][col] = num
            if resolve_sudoku(grid, row, col + 1):
                return True
        grid[row][col] = novalue
    return False

# Function to check if the number is valid in the row, column and square.
# It uses the check_row_column and check_square functions.
# It takes the number to be inserted and the coordinates.

def check_costraints(x: int, y: int, num: int):
    if check_row_column(x, y, num) and check_square(x, y, num):
        return True
    return False

# Function to check if the number is valid in the row and column.
# It takes the number to be inserted and the coordinates.

def check_row_column(x: int, y: int, num: int):
    for i in range(sudoku_size):
        if sudoku[y][i] == int(num) or sudoku[i][x] == int(num):
            return False
    return True

# Function to check if the number is valid in the square.
# It takes the number to be inserted and the coordinates.

def check_square(x: int, y: int, num: int):
    x = x // 3
    y = y // 3
    for i in range(y * 3, y * 3 + 3):
        for j in range(x * 3, x * 3 + 3):
            if sudoku[i][j] == int(num):
                return False
    return True

# Function that checks the number insertion from the user. 
# It checks:
#   - if the input is an integer
#   - if the input is between 1 and 9
#   - if the number is already present in the row or column
#   - if the number is already present in the square
# It returns a boolean and an error message. 
# If the insertion is valid, the boolean equals True and the error is None.
# If the insertion is not valid, the boolean equals False and an instance of the class
# error is created to add the correspondet message.
# It uses the check_row_column and check_square functions.
# It takes the number to be inserted and the coordinates.

def check_insert(x:int, y:int, num):
    if not num.isdigit():
        error = InsertionError("Number must be integer", pg.time.get_ticks())
        return False, error
    if int(num) > 9 or int(num) < 1:
        error = InsertionError("Number must be between 1 and 9", pg.time.get_ticks())
        return False, error
    if not check_row_column(x, y, int(num)):
        error = InsertionError("Already present in row or column", pg.time.get_ticks())
        return False, error
    if not check_square(x, y, int(num)):
        error = InsertionError("Already present in square", pg.time.get_ticks())
        return False, error
    return True, None
        
# Function to draw the lines of the sudoku.

def draw_lines():
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pg.draw.line(screen, black, (off_x, i * dif + off_y), (off_x + box_size, i * dif + off_y), thick)
        pg.draw.line(screen, black, (off_x + i * dif, off_y), (off_x + i * dif, box_size + off_y), thick)

# Function to draw the content of the sudoku.
# It checks if the number is inserted before the start of the game and, in that case,
# draws it in black. 
# If the number is inserted after the start of the game, it is drawn in blue.
# If the number is inserted in the helper mode, it is drawn in green.

def draw_content():
    for i in range(sudoku_size):
        for j in range(sudoku_size):
            if sudoku[i][j] != novalue:
                if not is_special[i][j]:
                    if is_inserted[i][j]:
                        text = number_font  .render(str(sudoku[i][j]), 1, black)
                        screen.blit(text, (off_x + j * dif + number_padding_x, off_y + i * dif + number_padding_y)) 
                    else:
                        text = number_font.render(str(sudoku[i][j]), 1, blue)
                        screen.blit(text, (off_x + j * dif + number_padding_x, off_y + i * dif + number_padding_y))
                else:
                    text = special_num_font.render(str(sudoku[i][j]), 1, green)
                    screen.blit(text, (off_x + j * dif + special_number_padding_x, off_y + i * dif + special_number_padding_y))

# Function to draw the buttons.

def draw_button(text: str, button_x: int, button_y: int):
    pg.draw.rect(screen, black, (button_x - start_button_border, button_y - start_button_border, button_width + end_button_border, button_height + end_button_border))
    pg.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    text = font.render(text, 1, white)
    text_rect = text.get_rect(center=(button_x + button_width/2, button_y + button_height/2))
    screen.blit(text, text_rect)

# Function to draw the error messages.

def draw_error_text(text: str):
    text = font.render(text, 1, black)
    text_rect = text.get_rect(center=(error_x, error_y))
    screen.blit(text, text_rect)

# Function to draw the coordinates of the sudoku clicked cell.

def draw_coord(x: int, y: int):
    text = font.render("x: " + str(x) + ", y: " + str(y), 1, black)
    text_rect = text.get_rect(center=(coord_x,  coord_y))
    screen.blit(text, text_rect)

#Function to draw the messages from the game.

def draw_message(message: str):
    text = font.render(message, 1, black)
    text_rect = text.get_rect(center=(message_x,  message_y))
    screen.blit(text, text_rect)

# Function to draw the end message.

def draw_finish():
    text = font.render("You finished, start again!", 1, black)
    text_rect = text.get_rect(center=(finish_x, finish_y))
    screen.blit(text, text_rect)

# Main loop of the game.
# It waits and checks the events to act accordingly.
# The events are:
#   - QUIT: to close the game
#   - MOUSEBUTTONDOWN: to check if the mouse is clicked
#   - KEYDOWN: to check if a key is pressed
# Mouse events:
#   - if the mouse is clicked on the start button, the game starts
#   - if the mouse is clicked on the solve button, the sudoku is solved
#   - if the mouse is clicked on the sudoku, the game waits for the user input and saves the coordinates
#   - if the mouse is clicked on the start again button, the game goes back to the original state
# Key events:
#   - if the key pressed is a number, the number is added to the user input
#   - if the key pressed is ENTER, the game tries to insert the number in the sudoku; if it can't an error is created
# It calls the functions to draw the elements of the game according to the state of the game. (If it started, which mode is active, etc.)
# It also checks if the game is finished and, in that case, it draws the end message.
# It updates the screen everytime an event occurs.

while True:
    event = pg.event.wait()

    if event.type == pg.QUIT:
        running = False
        pg.quit()
        sys.exit()  
    elif event.type == pg.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if start_button_x <= mouse_x <= start_button_x + button_width and start_button_y <= mouse_y <= start_button_y + button_height:
            if not start: 
                start = True
                num_input = ""
                inserting_x, inserting_y = None, None
            else:
                if not special_mode:
                    special_mode = True
                else:
                    is_special = np.full((sudoku_size, sudoku_size), False)
                    special_mode = False
        elif cancel_button_x <= mouse_x <= cancel_button_x + button_width and cancel_button_y <= mouse_y <= cancel_button_y + button_height:
            if start:
                if special_mode:
                    for i in range(sudoku_size):
                        for j in range(sudoku_size):
                            if is_special[i][j]:
                                sudoku[i][j] = novalue
                                is_special[i][j] = False
                                special_mode = False
        elif solve_button_x <= mouse_x <= solve_button_x + button_width and solve_button_y <= mouse_y <= solve_button_y + button_height:
            if special_mode:
                for i in range(sudoku_size):
                    for j in range(sudoku_size):
                        if is_special[i][j]:
                            sudoku[i][j] = novalue
                            is_special[i][j] = False
                            special_mode = False
            if resolve_sudoku(sudoku, 0, 0):
                solved = True
                start = False
                special_mode = False
                inserting_x, inserting_y = None, None
                num_input = ""
            else:
                error = InsertionError("Sudoku is not solvable", pg.time.get_ticks())
        elif off_x <= mouse_x <= off_x + box_size and off_y <= mouse_y <= off_y + box_size and not solved:
            temp_x = mouse_x - off_x
            temp_y = mouse_y - off_y
            inserting_x = temp_x // dif
            inserting_y = temp_y // dif
            if sudoku[inserting_y][inserting_x] != novalue and not start:
                sudoku[inserting_y][inserting_x] = novalue
                is_inserted[inserting_y][inserting_x] = False
                inserting_x, inserting_y = None, None
            elif is_inserted[inserting_y][inserting_x] and start:
                inserting_x, inserting_y = None, None
        elif start_again_x <= mouse_x <= start_again_x + button_width and start_again_y <= mouse_y <= start_again_y + button_height:
            sudoku = np.full((sudoku_size, sudoku_size), novalue)
            is_special = np.full((sudoku_size, sudoku_size), False)
            is_inserted = np.full((sudoku_size, sudoku_size), False)
            solved = False
            start = False
            special_mode = False
            inserting_x, inserting_y = None, None
            num_input = ""
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_BACKSPACE:
            num_input = num_input[:-1]
        else:
            if not inserting_x == None and not inserting_y == None:
                num_input += event.unicode
                result, error = check_insert(inserting_x, inserting_y, num_input)
                if result:
                    if not start:
                        sudoku[inserting_y][inserting_x] = int(num_input)
                        is_inserted[inserting_y][inserting_x] = True
                    elif start and not special_mode:
                        sudoku[inserting_y][inserting_x] = int(num_input)
                    elif start and special_mode:
                        sudoku[inserting_y][inserting_x] = int(num_input)
                        is_special[inserting_y][inserting_x] = True
                num_input = ""
                inserting_x, inserting_y = None, None

    screen.fill(white)
    draw_lines()
    draw_content()

    if inserting_x != None and inserting_y != None:
        draw_coord(inserting_x, inserting_y)

    if error and error.message != '':
        now_time = pg.time.get_ticks()
        if now_time - error.error_start >= 1500:
            error.message = ''
            error.error_start = 0
        else:
            draw_error_text(error.message)
    if not solved:
        draw_button("Solve", solve_button_x, solve_button_y)
        if not start:
            draw_message("Click on boxes to insert numbers")
            draw_button("Start game", start_button_x, start_button_y)
        else:
            if not special_mode:
                draw_button("Help mode", start_button_x, start_button_y)
            else:
                draw_button("Add changes", start_button_x, start_button_y)
                draw_button("Cancel", cancel_button_x, cancel_button_y)

    finished = True
    for i in range(sudoku_size):
        for j in range(sudoku_size):
            if sudoku[i][j] == novalue:
                finished = False
    if finished:
        draw_finish()
        draw_button("Start again", start_again_x, start_again_y)

    pg.display.flip()   