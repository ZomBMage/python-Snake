import screen
import max7219
import random
import keyboard
import time

device = max7219.matrix()

display = [[1 for i in range(32)]]
display.extend([[int((i/31).is_integer()) for i in range(32)]for j in range(6)])
display.append([1 for i in range(32)])
snake_pieces = [[0, [15,3]], [1, [16,3]], [2, [17,3]], [3, [18,3]]]
snake_direct = "left"
food_x = 0
food_y = 0
while (display[food_y][food_x] != 0):
    food_x = random.randint(1,30)
    food_y = random.randint(1,6)

display[food_y][food_x] = 1
for i in snake_pieces:
    display[i[1][1]][i[1][0]] = 1
dead = False
while not dead:
    dead = False
    if keyboard.is_pressed("down") and snake_direct != "up": snake_direct = "down"
    elif keyboard.is_pressed("up") and snake_direct != "down": snake_direct = "up"
    elif keyboard.is_pressed("left") and snake_direct != "right": snake_direct = "left"
    elif keyboard.is_pressed("right") and snake_direct != "left": snake_direct = "right"
    snake_pieces.pop(-1)
    snake_pieces = [[i[0]+1, i[1]] for i in snake_pieces]
    if snake_direct == "left":
        snake_pieces.append([0, [snake_pieces[0][1][0]-1, snake_pieces[0][1][1]]])
    elif snake_direct == "right":
        snake_pieces.append([0, [snake_pieces[0][1][0]+1, snake_pieces[0][1][1]]])
    elif snake_direct == "up":
        snake_pieces.append([0, [snake_pieces[0][1][0], snake_pieces[0][1][1]-1]])
    elif snake_direct == "down":
        snake_pieces.append([0, [snake_pieces[0][1][0], snake_pieces[0][1][1]+1]])
    snake_pieces = sorted(snake_pieces, key=lambda x: x[0])
    snake_head_x = snake_pieces[0][1][0]
    snake_head_y = snake_pieces[0][1][1]
    if snake_head_x == food_x and snake_head_y == food_y:
        snake_pieces = [[i[0]+1, i[1]] for i in snake_pieces]
        snake_pieces.append([0, [food_x,food_y]])        
        while (display[food_y][food_x] != 0):
            food_x = random.randint(1,30)
            food_y = random.randint(1,6)
    elif snake_head_x == 0:
        dead = True
    elif snake_head_y == 0:
        dead = True
    elif snake_head_x == 31:
        dead = True
    elif snake_head_y == 7:
        dead = True
    elif [snake_head_x, snake_head_y] in [i[1] for i in snake_pieces[1:]]:
        dead = True
    display = [[1 for i in range(32)]]
    display.extend([[int((i/31).is_integer()) for i in range(32)]for j in range(6)])
    display.append([1 for i in range(32)])
    display[food_y][food_x] = 1
    for i in snake_pieces:
        display[i[1][1]][i[1][0]] = 1
    
    commands = screen.output_to_screen(display)
    for command_set in commands:
        command_to_run = []
        for command in command_set:
            command_to_run.extend(command)
        print(command_to_run)
        device._write(command_to_run)

display = [[1]*32]*8
commands = screen.output_to_screen(display)
for command_set in commands:
    command_to_run = []
    for command in command_set:
        command_to_run.extend(command)
    device._write(command_to_run)
time.sleep(0.5)
display = [[0]*32]*8
commands = screen.output_to_screen(display)
for command_set in commands:
    command_to_run = []
    for command in command_set:
        command_to_run.extend(command)
    device._write(command_to_run)
print("Score:",len(snake_pieces))
quit()
