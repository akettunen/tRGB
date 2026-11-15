# COPYRIGHT (C) akettunen 2026
# imports
import turtle
import colorsys
import ctypes
import time
from PIL import Image, ImageDraw, ImageTk
import sys
# screen 
screen = turtle.Screen()
screen.title("Loading...")
screen.setup(width=600, height=600)
screen.bgcolor('black')
screen.colormode(1.0)
screen.tracer(0)
# title bar to dark
screen.update()
if sys.platform == "win32":
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
    if now - last >= 0.01:                       # per millisec
        screen.title(f"tRGB - {frames / (now - last):.1f} FPS")
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

# palette
STEPS = 600
palette = []
for k in range(STEPS):
    r, g, b = colorsys.hsv_to_rgb(k / STEPS, 1, 1)
    palette.append("#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255)))

step = STEPS // total
SUB = 2
NFRAMES = STEPS // SUB

# prerender every frame
MARGIN = 10
minx = -side / 2 - MARGIN
maxy = 2 * h / 3 + MARGIN
W = int(side + 2 * MARGIN)
H = int(h + 2 * MARGIN)
def to_px(p):
    return (p[0] - minx, maxy - p[1])
cpx = to_px(center)
pts_px = [to_px(p) for p in points]
R = 7.5

def render(base):
    img = Image.new("RGB", (W, H), "black")
    d = ImageDraw.Draw(img)
    # rainbow effect 1
    for i in range(total):
        s, j = divmod(i, pieces)
        p1 = pts_px[s * (pieces + 1) + j]
        p2 = pts_px[s * (pieces + 1) + j + 1]
        c = palette[(i * step + base) % STEPS]
        d.polygon([cpx, p1, p2], fill=c, outline=c)
    # rainbow effect 2
    for i in range(total):
        s, j = divmod(i, pieces)
        p1 = pts_px[s * (pieces + 1) + j]
        p2 = pts_px[s * (pieces + 1) + j + 1]
        c = palette[(i * step + base) % STEPS]
        d.line([p1, p2], fill=c, width=15)
        for x, y in (p1, p2):
            d.ellipse([x - R, y - R, x + R, y + R], fill=c)
    return ImageTk.PhotoImage(img)

raw = cv._canvas
frames_img = [render(f * SUB) for f in range(NFRAMES)]
# x, y
img_x = minx + W / 2
img_y = -(maxy - H / 2)
item = raw.create_image(img_x, img_y, image=frames_img[0])

# clean exit
running = True
def on_close():
    global running
    running = False
screen._root.protocol("WM_DELETE_WINDOW", on_close)

current = 0
itemconfigure = raw.itemconfigure
update = screen._root.update
clock = time.perf_counter

def draw_frame():
    global current
    idx = int(offset * NFRAMES) % NFRAMES
    if idx != current:               # only touch the canvas when the image changes
        itemconfigure(item, image=frames_img[idx])
        current = idx
    update()
    update_fps()

SPEED = 0.32 # change cycle speed (higher=faster)

start = clock()
while running:
    offset = ((clock() - start) * SPEED) % 1
    try:
        draw_frame()
    except Exception:
        break
