import font,time
# Placeholder screen - for programs to use as an arbitrary 32x8 display
screen = [[0 for i in range(32)] for j in range(8)]

def break_screens(screen):
    """This function splits a matrix into 8x8 matrices"""
    matrices = []
    for i in range(int(len(screen[0])/8)):
        temp_matrix = []
        for j in range(8):
            # For each set of 8 columns along the matrix
            temp_matrix.append(screen[j][i*8:(i+1)*8])
        matrices.append(temp_matrix)
    return matrices

def join_screens(matrices):
    """This function joins 8x8 matrices into one matrix"""
    screen = []
    for k in range(8):
        row = []
        for matrix in matrices:
            row.extend(matrix[k])
        screen.append(row)
    return screen

def sub_char(screen, character, matrix):
    """This replaces one matrix in the screen with a character or pattern"""
    matrices = break_screens(screen)
    # The below line turns the stored font format into a 8x8 binary matrix
    character = [[int(i) for i in str(bin(j))[2:].zfill(8)] for j in character]
    matrices[matrix] = character
    screen = join_screens(matrices)
    return screen

def gen_screen_from_num(screen,num):
    """This function makes a 32x8 screen for any number between 0 and 9999"""
    if num >= 0 and num < 10000:
        if num < 10: # Leading zeroes are replaced with empty space
            screen = sub_char(screen, font.patterns.empty, 0)
            screen = sub_char(screen, font.patterns.empty, 1)
            screen = sub_char(screen, font.patterns.empty, 2)
            screen = sub_char(screen, getattr(font.numbers, "digit_"+str(num)), 3)
        elif num < 100:
            screen = sub_char(screen, font.patterns.empty, 0)
            screen = sub_char(screen, font.patterns.empty, 1)
            for i in enumerate(str(num)):
                screen = sub_char(screen, getattr(font.numbers, "digit_"+i[1]), i[0]+2)
        elif num < 1000:
            screen = sub_char(screen, font.patterns.empty, 0)
            for i in enumerate(str(num)):
                screen = sub_char(screen, getattr(font.numbers, "digit_"+i[1]), i[0]+1)
        else:
            for i in enumerate(str(num)):
                screen = sub_char(screen, getattr(font.numbers, "digit_"+i[1]), i[0])
    return screen

def output_to_screen(screen):
    """Returns a series of commands to display the screen"""
    commands = []
    for row in enumerate(screen):
        temp_commands = []
        for i in range(0,len(row[1]),8):
            # For each row in each matrix of the screen turn it
            # into a register and a data value
            data = row[1][i: i+8]
            data = "".join(map(str, data)) # Connect each bit into a binary
            data = int(data, base=2)       # string and convert to base 10
            register = row[0] + 1
            temp_commands.append([register,data])
        commands.append(temp_commands)
    return commands

def show_message(device, message, delay=0, endpad=True):
    """Display a scrolling message on the device given"""
    # Due to processing overheads this now displays each command as
    # it is produced. There was a significant delay when producing
    # the "screen" to scroll along
    message = "    "+message.upper() # Padding is needed so that it scrolls on
    if endpad:
        message = message + "    "

    # The below line generates a blank screen with a matrix for each character
    scrolling_screen = [[0 for i in range(8*len(message))] for j in range(8)]
    # For each letter:
    for i in enumerate(message):
        # Getattr is a method used here to get a property of an object through
        # a string. This removes the need for conditional statements for each
        # character. Sadly this is unavoidable with special characters.
        if i[1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            scrolling_screen = sub_char(scrolling_screen, getattr(font.letters, "letter_"+i[1]), i[0])
        elif i[1] in "0123456789":
            scrolling_screen = sub_char(scrolling_screen, getattr(font.numbers, "digit_"+i[1]), i[0])
        elif i[1] == "!":
            scrolling_screen = sub_char(scrolling_screen, font.special.exclamation_mark, i[0])
        elif i[1] == "\"":
            scrolling_screen = sub_char(scrolling_screen, font.special.quotation_mark, i[0])
        elif i[1] == "#":
            scrolling_screen = sub_char(scrolling_screen, font.special.hashtag, i[0])
        elif i[1] == "$":
            scrolling_screen = sub_char(scrolling_screen, font.special.dollar_sign, i[0])
        elif i[1] == "%":
            scrolling_screen = sub_char(scrolling_screen, font.special.percent_sign, i[0])
        elif i[1] == "&":
            scrolling_screen = sub_char(scrolling_screen, font.special.ampersand, i[0])
        elif i[1] == "'":
            scrolling_screen = sub_char(scrolling_screen, font.special.apostraphe, i[0])
        elif i[1] == "(":
            scrolling_screen = sub_char(scrolling_screen, font.special.bracket_left, i[0])
        elif i[1] == ")":
            scrolling_screen = sub_char(scrolling_screen, font.special.bracket_right, i[0])
        elif i[1] == "*":
            scrolling_screen = sub_char(scrolling_screen, font.special.asterisk, i[0])
        elif i[1] == "+":
            scrolling_screen = sub_char(scrolling_screen, font.special.plus_sign, i[0])
        elif i[1] == ",":
            scrolling_screen = sub_char(scrolling_screen, font.special.comma, i[0])
        elif i[1] == ".":
            scrolling_screen = sub_char(scrolling_screen, font.special.full_stop, i[0])
        elif i[1] == "-":
            scrolling_screen = sub_char(scrolling_screen, font.special.hyphen, i[0])
        elif i[1] == "/":
            scrolling_screen = sub_char(scrolling_screen, font.special.slash, i[0])
        elif i[1] == ":":
            scrolling_screen = sub_char(scrolling_screen, font.special.colon, i[0])
        elif i[1] == ";":
            scrolling_screen = sub_char(scrolling_screen, font.special.semicolon, i[0])
        elif i[1] == "<":
            scrolling_screen = sub_char(scrolling_screen, font.special.less_than_sign, i[0])
        elif i[1] == ">":
            scrolling_screen = sub_char(scrolling_screen, font.special.greater_than_sign, i[0])
        elif i[1] == "=":
            scrolling_screen = sub_char(scrolling_screen, font.special.equal_sign, i[0])
        elif i[1] == "?":
            scrolling_screen = sub_char(scrolling_screen, font.special.question_mark, i[0])
        else:
            scrolling_screen = sub_char(scrolling_screen, font.patterns.empty, i[0])
    
    command_list = []
    # The following for loop simulates a 32x8 buffer scrolling along the
    # generated screen, one column at a time, and generates commands for each
    # "display" at each position.
    for i in range(len(scrolling_screen[0])-32):
        screen = [scrolling_screen[row][i:i+32] for row in range(8)]
        commands = output_to_screen(screen)
        for command_set in enumerate(commands):
            command_to_run = []
            for command in command_set[1]:
                command_to_run.extend(command)
            device._write(command_to_run)
            if command_set[0] % 8 ==0:
                time.sleep(delay) # This is optional to control the scroll speed
