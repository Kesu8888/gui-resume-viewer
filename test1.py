import tkinter as tk
from PIL import ImageOps
import sys
from PIL import Image, ImageTk
from pathlib import Path
import ctypes

pic_cwd = sys.path[0] + "\\pic\\" + "ImageViewer//"
ctypes.windll.shcore.SetProcessDpiAwareness(1)


def change_on_hover(canvas, button, image_leave, image_enter):
    canvas.tag_bind(button, '<Enter>', lambda x: canvas.itemconfig(button, image=image_enter))
    canvas.tag_bind(button, '<Leave>', lambda x: canvas.itemconfig(button, image=image_leave))
    canvas.tag_bind(button, '<Button-1>', lambda x: canvas.config(background="blue"))

root = tk.Tk()
root.geometry("1440x900+400+400")
frame = tk.Frame(root, background="green")
frame.pack(fill='both', expand=True)
canvas = tk.Canvas(frame, background="red", width=400, height=400)
canvas.place(x=0, y=0, anchor="nw")
img_active = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonRightActive.png"))
img_change = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonRightChange.png"))
img_Disable = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonRightDisable.png"))
button = canvas.create_image(0, 0, image=img_active, anchor='nw')
change_on_hover(canvas=canvas, button=button, image_enter=img_change, image_leave=img_active)
button_new = canvas.create_image(0, 0, image=img_Disable, anchor='nw')
canvas.tag_bind(button_new, '<Button-1>', lambda x: canvas.delete(button_new))

root.mainloop()


