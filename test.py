import tkinter as tk
from PIL import ImageOps
import sys
from PIL import Image, ImageTk
from pathlib import Path
import ctypes

pic_cwd = sys.path[0] + "\\pic\\"
ctypes.windll.shcore.SetProcessDpiAwareness(1)


root = tk.Tk()
root.geometry("1440x900+300+200")
frame = tk.Frame(root)
frame.grid(sticky="nsew")
canvas = tk.Canvas(frame, background="red", width=1440, height=900)
canvas.pack(fill='both', expand=True)

img_active = ImageTk.PhotoImage(file=pic_cwd+"buttonLeftActive.png")
img_disable = ImageTk.PhotoImage(file=pic_cwd+"buttonLeftDisable.png")


def change_on_hover1(canv, obj1, img):
    print("1")
    canv.itemconfig(obj1, image=img)
    # canv.tag_bind(obj1, '<Leave>', lambda x: change_on_hover2(canv, obj1, img))


def change_on_hover2(canv, obj1, img):
    print("2")
    canv.itemconfig(obj1, image=img)
    # canv.tag_bind(obj1, '<Enter>', lambda x: change_on_hover1(canv, obj1, img))


def show_pic(canv, x, y, img):
    canv.create_image((x, y), image=img, anchor='center')

button = canvas.create_image((200, 200), image=img_active, anchor='center')
canvas.tag_bind(button, '<Enter>', lambda x: change_on_hover1(canvas, button, img_disable))
canvas.tag_bind(button, '<Leave>', lambda x: change_on_hover2(canvas, button, img_active))
canvas.tag_bind(button, '<Button-1>', lambda x: show_pic(canvas, 300, 300, img_active))

root.mainloop()



