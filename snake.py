# Import libraries
import screen
import max7219
import random
import keyboard
import time

# Initialise device
device = max7219.matrix()

# Create a digitally stored display
display = [[1 for i in range(32)]]
# The following line generates 6 lines of 1000...0001
display.extend([[int((i/31).is_integer()) for i in range(32)]for j in range(6)])
display.append([1 for i in range(32)])

# Initialise the snake as 4 pieces with each having coordinates
snake_pieces = [[0, [15,3]], [1, [16,3]], [2, [17,3]], [3, [18,3]]]
snake_direct = "left"

# Generate a food location somewhere in the 0s in the display
food_x = 0
food_y = 0
while (display[food_y][food_x] != 0):
    food_x = random.randint(1,30)
    food_y = random.randint(1,6)

display[food_y][food_x] = 1

# Display the snake
for i in snake_pieces:
    display[i[1][1]][i[1][0]] = 1

# Start the game by outputting the first display
dead = False
commands = screen.output_to_screen(display)
for command_set in commands:             # This turns the output of 
    command_to_run = []                  # screen.output_to_screen
    for command in command_set:          # into sets of 4 commands
        command_to_run.extend(command)   # to load each row into the
    device._write(command_to_run)        # device


while not dead: # Let's play
    dead = False

    # Check if the user changes the direction of the snake
    # This also prevents doing a 180 degree turn, killing you instantly
    if keyboard.is_pressed("down") and snake_direct != "up": snake_direct = "down"
    elif keyboard.is_pressed("up") and snake_direct != "down": snake_direct = "up"
    elif keyboard.is_pressed("left") and snake_direct != "right": snake_direct = "left"
    elif keyboard.is_pressed("right") and snake_direct != "left": snake_direct = "right"
    
    # The snake moves by removing its last piece and creating a new head
    snake_pieces.pop(-1)
    snake_pieces = [[i[0]+1, i[1]] for i in snake_pieces] # Increment piece IDs
    if snake_direct == "left":
        snake_pieces.append([0, [snake_pieces[0][1][0]-1, snake_pieces[0][1][1]]])
    elif snake_direct == "right":
        snake_pieces.append([0, [snake_pieces[0][1][0]+1, snake_pieces[0][1][1]]])
    elif snake_direct == "up":
        snake_pieces.append([0, [snake_pieces[0][1][0], snake_pieces[0][1][1]-1]])
    elif snake_direct == "down":
        snake_pieces.append([0, [snake_pieces[0][1][0], snake_pieces[0][1][1]+1]])
    # The snake pieces need to be sorted otherwise the head gets removed
    snake_pieces = sorted(snake_pieces, key=lambda x: x[0])
    snake_head_x = snake_pieces[0][1][0]
    snake_head_y = snake_pieces[0][1][1]
    # Check if snake has eaten food
    if snake_head_x == food_x and snake_head_y == food_y:
        snake_pieces = [[i[0]+1, i[1]] for i in snake_pieces]
        snake_pieces.append([0, [food_x,food_y]])        
        while (display[food_y][food_x] != 0):
            food_x = random.randint(1,30)
            food_y = random.randint(1,6)
    # Check if the snake is dead
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
    # Regenerate the display in the same method as before
    display = [[1 for i in range(32)]]
    display.extend([[int((i/31).is_integer()) for i in range(32)]for j in range(6)])
    display.append([1 for i in range(32)])
    display[food_y][food_x] = 1
    for i in snake_pieces:
        display[i[1][1]][i[1][0]] = 1
    
    # Draw the new display on the matrix
    commands = screen.output_to_screen(display)
    for command_set in commands:
        command_to_run = []
        for command in command_set:
            command_to_run.extend(command)
        device._write(command_to_run)

# Make all of the LEDs turn on briefly
display = [[1]*32]*8
commands = screen.output_to_screen(display)
for command_set in commands:
    command_to_run = []
    for command in command_set:
        command_to_run.extend(command)
    device._write(command_to_run)
# Show some scrolling messages to show the end of the game
screen.show_message(device, "Game over!")
screen.show_message(device, "Your score:   {}".format(len(snake_pieces)-4),0,False)
time.sleep(2)

# Wipe the screen
screen.show_message(device,"")
# Fin.
