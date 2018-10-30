from tkinter import *
from PIL import Image,ImageTk
import keyboard
from points import CreatePoints
root = Tk()
root.resizable(FALSE, FALSE)


def subimage(l, t, r, b):
    imageFile = Image.open(r"images/pacmanspritesheet2.png")
    cropped =imageFile.crop((l,t,r,b))
    return cropped


def updateimage(sprite):
    global last_img
    global x
    global y
    global dx
    global dy
    global last_img_pil
    global top_left, top_right, right_top, right_bottom, bottom_left, bottom_right, left_bottom, left_top
    canvas.delete(last_img)
    checkKeyboard()
    x += dx
    y += dy

    for p in set(points):
        if abs(x - canvas.coords(p)[0]) < 20 and abs(y - canvas.coords(p)[1]) < 20:
            canvas.delete(p)
            points.remove(p)



    top_left[0], top_left[1] = top_left[0] + dx, top_left[1] + dy
    top_right[0], top_right[1] = top_right[0] + dx, top_right[1] + dy
    right_top[0], right_top[1] = right_top[0] + dx, right_top[1] + dy
    right_bottom[0], right_bottom[1] = right_bottom[0] + dx, right_bottom[1] + dy
    bottom_right[0], bottom_right[1] = bottom_right[0] + dx, bottom_right[1] + dy
    bottom_left[0], bottom_left[1] = bottom_left[0] + dx, bottom_left[1] + dy
    left_bottom[0], left_bottom[1] = left_bottom[0] + dx, left_bottom[1] + dy
    left_top[0], left_top[1] = left_top[0] + dx, left_top[1] + dy

    last_img_pil = ImageTk.PhotoImage(images[sprite].rotate(angle))
    last_img = canvas.create_image(x % 672,y, image=last_img_pil)
    root.after(40, updateimage, (sprite+1) % num_sprites)


def checkKeyboard():
    global dx
    global dy
    global angle
    global map_pixels
    global top_left, top_right, right_top, right_bottom, bottom_left, bottom_right, left_bottom, left_top
    global next_move

    #if keypressed or next move is key and one of the sides is clear and moving to the respective direction => change dx/y accordingly
    if (keyboard.is_pressed('d') or next_move == 'd') and \
       ((map_pixels[right_bottom[0], right_bottom[1]] != (0, 120, 248, 255)) and
       (map_pixels[right_top[0], right_top[1]] != (0, 120, 248, 255))):

        dx = 8

        dy = 0
        angle = 0
        next_move = None
    elif (keyboard.is_pressed('w') or next_move == 'w') and \
         ((map_pixels[top_right[0], top_right[1]] != (0, 120, 248, 255)) and
         (map_pixels[top_left[0],top_left[1]] != (0,120,248,255))):

        dx = 0
        dy = -8
        angle = 90
        next_move = None
    elif (keyboard.is_pressed('a') or next_move == 'a') and \
         ((map_pixels[left_top[0], left_top[1]] != (0, 120, 248, 255)) and
         (map_pixels[left_bottom[0],left_bottom[1]] != (0,120,248,255))):

        dx = -8
        dy = 0
        angle = 180
        next_move = None
    elif (keyboard.is_pressed('s') or next_move == 's') and \
         ((map_pixels[bottom_right[0], bottom_right[1]] != (0, 120, 248, 255)) and
         (map_pixels[bottom_left[0],bottom_left[1]] != (0,120,248,255))):

        dx = 0
        dy = 8
        angle = 270
        next_move = None

    #if block ahead and dx/y is moving into block => reset dx/y
    if (map_pixels[right_bottom[0],right_bottom[1]] == (0, 120, 248, 255) or
        map_pixels[right_top[0],right_top[1]] == (0, 120, 248, 255)) and dx == 8:
        dx = 0
    if (map_pixels[left_top[0], left_top[1]] == (0, 120, 248, 255) or
        map_pixels[left_bottom[0], left_bottom[1]] == (0, 120, 248, 255)) and dx == -8:
        dx = 0
    if (map_pixels[top_left[0], top_left[1]] == (0, 120, 248, 255) or
        map_pixels[top_right[0], top_right[1]] == (0, 120, 248, 255)) and dy == -8:
        dy = 0
    if (map_pixels[bottom_left[0], bottom_left[1]] == (0, 120, 248, 255) or
        map_pixels[bottom_right[0], bottom_right[1]] == (0, 120, 248, 255)) and dy == 8:
        dy = 0

    #if keypressed and blocked to the same direction => save next move
    if keyboard.is_pressed('d') and (map_pixels[right_bottom[0],right_bottom[1]] == (0, 120, 248, 255) or
                                     map_pixels[right_top[0],right_top[1]] == (0, 120, 248, 255)):
        next_move = 'd'

    elif keyboard.is_pressed('w') and (map_pixels[top_left[0], top_left[1]] == (0, 120, 248, 255) or
                                       map_pixels[top_right[0], top_right[1]] == (0, 120, 248, 255)):
        next_move = 'w'
    elif keyboard.is_pressed('a') and (map_pixels[left_top[0], left_top[1]] == (0, 120, 248, 255) or
                                       map_pixels[left_top[0], left_top[1]] == (0, 120, 248, 255)):
        next_move = 'a'
    elif keyboard.is_pressed('s') and (map_pixels[bottom_left[0], bottom_left[1]] == (0, 120, 248, 255) or
                                       map_pixels[bottom_right[0], bottom_right[1]] == (0, 120, 248, 255)):
        next_move = 's'


next_move = None
checker_offset = 9
preoffset = 21
num_sprites = 3
last_img = None
images = [subimage(43*i, 29, 43*(i+1), 72) for i in range(num_sprites)]

canvas = Canvas(width=672, height=884,bg = "black")
canvas.pack()
imageFile2 = Image.open(r"images/pacmanmap3.png")
map_pixels = imageFile2.load() # (0, 120, 248, 255) is blue (wall) and (0, 0, 0, 0) is black (free space)
mapBG = ImageTk.PhotoImage(imageFile2)
x = 335
y = 665
 # I need to re-create this into 8 points instead of 4 points, top left, top right, right top, right bottom, bottom right, bottom left, left bottom and left top.
 # the best number to add or subtract is 20!!

top_left = [x-preoffset, y-43/2-checker_offset]
top_right = [x+preoffset, y-43/2-checker_offset]
right_top = [x+43/2+checker_offset, y-preoffset]
right_bottom = [x+43/2+checker_offset, y+preoffset]
bottom_right = [x+preoffset, y+43/2+checker_offset]
bottom_left = [x-preoffset, y+43/2+checker_offset]
left_bottom = [x-43/2-checker_offset, y-preoffset]
left_top = [x-43/2-checker_offset, y+preoffset]


dx = 0
dy = 0
angle = 0
canvas.create_image(672 / 2, 884 / 2, image=mapBG)
points = CreatePoints(canvas)
updateimage(0)
mainloop()