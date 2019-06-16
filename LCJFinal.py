"""
The program allows you to enter images into a list, which can then be selected
as a colour scheme for randomly drawn dots and lines to create a screen saver
effect.
It uses the turtle library for drawing, Pillow to deal with images and colours
and finally tkinter as the UI for which to interact with and watch the program.
"""

import turtle
import random
import tkinter as tk
from tkinter import TclError
from PIL import Image
from collections import defaultdict

root = tk.Tk()
canvas = tk.Canvas(master=root, width=1500, height=700)
canvas.pack()

t_screen = turtle.TurtleScreen(canvas)
rt = turtle.RawTurtle(t_screen)

t_screen.bgcolor("black")
t_screen.colormode(255)

dots = 100000  # Controls for loop length which runs the program
rt.speed(0)
rt.pensize(80)
rt.shape('turtle')

# The photos were saved within the project folder. Please use .png files
photo_lib = ['bathbomb1.png',
             'bathbomb2.png',
             'bathbomb3.png']

palette = defaultdict(int)
mp = [(0, 0, 0)]


def img_control(choice):
    """
    :param choice: This is passed by the buttons which select the colour scheme

    img_control clears the previous colour lists and dictionaries and refreshes
    it with the selected images colours.
    """
    mp.clear()
    palette.clear()
    im = Image.open(photo_lib[choice])

    for pixel in im.getdata():
        palette[pixel] += 1

    try:
        for a, b, c, d in palette.keys():
            rgb_scheme = (a, b, c)
            mp.append(rgb_scheme)

    except ValueError:
        for a, b, c in palette.items():
            rgb_scheme = (a, b, c)
            mp.append(rgb_scheme)


# All three following functions are just to pass a value into img_control
def bb1():
    img_control(0)


def bb2():
    img_control(1)


def bb3():
    img_control(2)


# The next two functions allow the sliders to control pen speed and size
def speed_control(set_speed):
    int_speed = int(set_speed)
    rt.speed(int_speed)


def size_control(thickness):
    int_thickness = int(thickness)
    rt.pensize(int_thickness)


def show_hide():
    """
     Hides or shows the turtle upon checkbox tick.
    """
    if rt.isvisible():
        rt.hideturtle()
    else:
        rt.showturtle()


tk.Button(master=root, text='Melusine', command=bb1).place(x=15, y=715)
tk.Button(master=root, text='Golden Pear', command=bb2).place(x=100, y=715)
tk.Button(master=root, text='Giant Rose', command=bb3).place(x=205, y=715)

tk.Scale(master=root, from_=0, to_=10, orient='horizontal',
         command=speed_control).pack(side='right')
tk.Label(master=root, text='Speed:').place(x=1370, y=705)

scale = tk.Scale(master=root, from_=0, to_=150, sliderlength=40,
                 orient='horizontal', length=400, command=size_control)
scale.set(80)
scale.pack(side='bottom')

tk.Label(master=root, text='Pen Size: ').place(x=460, y=705)

tk.Checkbutton(master=root, text='Hide Turtle?',
               command=show_hide).place(x=300, y=715)


def move():
    """
    Firstly gives the turtle a destination within the canvas.
    Secondly the dot may become a line if 96 or greater is rolled from 100.
    Finally based on the destination, a randomly sized circle may be drawn

    """
    destination = [random.randrange(-750, 750), random.randrange(-350, 350)]

    rt.penup()
    rt.setpos(destination[0], destination[1])
    rt.pencolor(random.choice(mp))

    slodge = random.randint(1, 100)
    length = 1

    if slodge >= 96:
        length = 100

    elif slodge != 100:
        length = 1

    if destination[1] >= 250:
        rt.pendown()
        rt.backward(length)

    if 250 > destination[1] > -100:
        rt.pendown()
        rt.forward(length)

    if destination[1] <= -100:
        rt.pendown()
        rt.backward(length)

    """
    This if statement is an example of an 'event zone' where the turtle may
    behave uniquely if you wish. 
    if 100 > destination[0] > 0 and 100 > destination[1] > 0:
        rt.pendown()
        rt.forward(1)
        rt.circle(40)
    """

    if destination[0] % random.randint(16, 19) == 0:
        rt.pendown()
        rt.forward(1)
        rt.circle(random.randint(15, 30))

    if destination[1] % random.randint(11, 14) == 0:
        rt.pendown()
        rt.right(random.randint(20, 160))
        rt.circle(random.randint(15, 30))


try:
    for i in range(dots):
        move()

    tk.mainloop()

except TclError:
    print("_tkinter.TclError: invalid command name .!canvas")
