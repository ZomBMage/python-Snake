import font
screen = [[0 for i in range(32)] for j in range(8)]
def printscr(screen):
    for i in screen:
        print(i)

def break_screens(screen):
    matrices = []
    for i in range(int(len(screen[0])/8)):
        temp_matrix = []
        for j in range(8):
            temp_matrix.append(screen[j][i*8:(i+1)*8])
        matrices.append(temp_matrix)
    return matrices

def join_screens(matrices):
    screen = []
    for k in range(8):
        row = []
        for matrix in matrices:
            row.extend(matrix[k])
        screen.append(row)
    return screen

def sub_char(screen, character, matrix):
    matrices = break_screens(screen)
    character = [[int(i) for i in str(bin(j))[2:].zfill(8)] for j in character]
    matrices[matrix] = character
    screen = join_screens(matrices)
    return screen

def gen_screen_from_num(screen,num):
    if num >= 0 and num < 10000:
        if num < 10:
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
            data = row[1][i: i+8]
            data = "".join(map(str, data))
            data = int(data, base=2)
            register = row[0] + 1
            temp_commands.append([register,data])
        commands.append(temp_commands)
    return commands

def show_message(screen, message):
    message = "    "+message.upper()+"    "
    scrolling_screen = [[0 for i in range(8*len(message)+8)] for j in range(8)]
    for i in enumerate(message):
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
    for i in range(len(scrolling_screen[0])-32):
        screen = [scrolling_screen[row][i:i+32] for row in range(8)]
        print(screen)
        command_list.extend(output_to_screen(screen))
    
    return command_list


show_message(screen, "Hello world!")