import max7219
import font
import screen

device = max7219.matrix()

for i in range(10000):
    display = screen.gen_screen_from_num(display, i)
    commands = screen.output_to_screen(display)
    for command_set in commands:
        command_to_run = []
        for command in command_set:
            command_to_run.extend(command)
        device._write(command_to_run)