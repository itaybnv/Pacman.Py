from tkinter import *
from PIL import ImageTk, Image


def subimage(l, t, r, b):
    imageFile = Image.open(r"images/pacmanspritesheet2.png")
    cropped = imageFile.crop((l,t,r,b))
    return cropped


def CreatePoints(canvas):
    global point_pil
    points = []
    point_pil = ImageTk.PhotoImage(subimage(8, 8, 14, 14))

    # (50,825) - (615,825)
    for point in range(26):

        points.append(canvas.create_image(50 + point * 23,825,image=point_pil))

    for point in range(4):
        points.append(canvas.create_image(50,825 - point * 21,image=point_pil))

    for point in range(6):
        points.append(canvas.create_image(50 + point * 25,762,image=point_pil))

    for point in range(26):
        points.append(canvas.create_image(175,762 - point * 28,image=point_pil))

    for point in range(13):
        points.append(canvas.create_image(45+ point * 21.5,62,image=point_pil))

    for point in range(9):
        points.append(canvas.create_image(45,62 + point * 28,image=point_pil))

    for point in range(26):
        if point != 5:
            points.append(canvas.create_image(67 + point * 22,185,image=point_pil))

    for point in range(5):
        points.append(canvas.create_image(64 + point * 23,285.5,image=point_pil))





    return points
