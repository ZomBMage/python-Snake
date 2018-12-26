import font
screen = [[0 for i in range(32)] for j in range(8)]
def printscr(screen):
    for i in screen:
        print(i)

def break_screens(screen):
    matrices = []
    for i in range(4):
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
            data = hex(data)
            register = row[0] + 1
            temp_commands.append([register,data])
        commands.append(temp_commands[::-1])
    return commands