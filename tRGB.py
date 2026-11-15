# COPYRIGHT (C) akettunen 2026
# imports
import turtle
import colorsys
import ctypes
import time
# title

# screen 
screen = turtle.Screen()
screen.title("trianRGBle")
screen.setup(width=600, height=600)
screen.bgcolor('black')
screen.colormode(1.0)
screen.tracer(0)
# title bar to dark
screen.update()
hwnd = ctypes.windll.user32.GetParent(screen._root.winfo_id())
ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(1)), 4)
# canvas 
cv = screen.getcanvas()
cv.config(bg='black', highlightthickness=0, bd=0)
cv._canvas.config(bg='black', highlightthickness=0, bd=0)
cv._canvas.grid_configure(padx=0, pady=0)
cv.hscroll.grid_remove()
cv.vscroll.grid_remove()
screen._root.config(bg='black')
# turtle
t = turtle.Turtle()
t.hideturtle()
# things
side = 300
pieces = 40                      
h = side * 3 ** 0.5 / 2
# fps
frames = 0
last = time.time()
def update_fps():
    global frames, last
    frames += 1
    now = time.time()
    if now - last >= 1:                       # per sec
        screen.title(f"trianRGBle - {frames / (now - last):.1f} FPS")
        frames = 0
        last = now
# triangle corners and center
A = (-side / 2, -h / 3)
B = (side / 2, -h / 3)
C = (0, 2 * h / 3)
center = (0, 0)
corners = [A, B, C, A]

total = pieces * 3
offset = 0

def lerp(p, q, k):
    return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)

# all points ready
points = []
for s in range(3):
    for j in range(pieces + 1):
        points.append(lerp(corners[s], corners[s + 1], j / pieces))

def draw_frame():
    global offset
    t.clear()
    i = 0
    # rainbow effect 1
    t.width(1)
    for s in range(3):
        for j in range(pieces):
            p1 = points[s * (pieces + 1) + j]
            p2 = points[s * (pieces + 1) + j + 1]
            color = colorsys.hsv_to_rgb((i / total + offset) % 1, 1, 1)
            t.color(color)
            t.penup()
            t.goto(center)
            t.pendown()
            t.begin_fill()
            t.goto(p1)
            t.goto(p2)
            t.goto(center)
            t.end_fill()
            i += 1

    # rainbow effect 2
    t.width(15)
    i = 0
    for s in range(3):
        for j in range(pieces):
            p1 = points[s * (pieces + 1) + j]
            p2 = points[s * (pieces + 1) + j + 1]
            t.pencolor(colorsys.hsv_to_rgb((i / total + offset) % 1, 1, 1))
            t.penup()
            t.goto(p1)
            t.pendown()
            t.goto(p2)
            i += 1

    screen.update()
    update_fps()
    offset = (offset + 0.005) % 1
    screen.ontimer(draw_frame, 20)

draw_frame()
turtle.done()