import tkinter as tk
from PIL import ImageOps
import sys
from PIL import Image, ImageTk
from pathlib import Path
import ctypes

pic_cwd = sys.path[0] + "\\pic\\"
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Centre(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Initialize the TK object
        win_width = (self.winfo_screenwidth()-1440)/2
        win_height = (self.winfo_screenheight()-900)/2
        self.title('resume')
        self.iconbitmap(pic_cwd + "thumbs-up.ico")
        self.geometry("1440x900" + "+" + str(int(win_width)) + "+" + str(int(win_height)))
        self.resizable(False, False)

        # Create container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing frames to an empty array
        self.frames = {}

        for F in (MenuFrame, AcademicFrame, PgFrame, SkillFrame, HobbyFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MenuFrame)

    def show_frame(self, frame_name):
        print(frame_name.__name__)
        change_frame = self.frames[frame_name]
        change_frame.tkraise()


def change_on_hover(button, image_leave, image_enter):
    button.bind("<Enter>", lambda e: button.config(image=image_enter))
    button.bind("<Leave>", lambda e: button.config(image=image_leave))


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Adding background image
        self.img = Image.open(pic_cwd + "MenuFrameBg.jpg")
        self.bg_img = ImageTk.PhotoImage(self.img)
        wall_paper = tk.Label(self, image=self.bg_img, highlightthickness=0)
        wall_paper.place(x=0, y=0)

        # Creating four buttons for academicFrame, HobbyFrame, PgFrame, SkillFrame
        x = [505, 735, 500, 735]
        y = [440, 440, 600, 600]
        i = 0
        self.buttons = {}
        commands=[lambda:controller.show_frame(AcademicFrame), lambda:controller.show_frame(PgFrame),lambda:controller.show_frame(SkillFrame), lambda:controller.show_frame(HobbyFrame)]
        for F in (AcademicFrame, PgFrame, SkillFrame, HobbyFrame):
            im = Image.open(pic_cwd + F.__name__ + "Button.png")
            self.button_image = ImageTk.PhotoImage(im)
            self.buttons[F] = tk.Button(self, image=self.button_image, borderwidth=0, highlightthickness=0,
                                    background="white",
                                    command=commands[i])
            self.button_change = ImageTk.PhotoImage(Image.open(pic_cwd + F.__name__ + "Change.png"))
            change_on_hover(self.buttons[F], self.button_image, self.button_change)
            self.buttons[F].place(x=x[i], y=y[i])
            i += 1


class AcademicFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Adding background image
        self.img = Image.open(pic_cwd + "AcademicFrame" + "Bg.jpg")
        self.bg_img = ImageTk.PhotoImage(self.img)
        wall_paper = tk.Label(self, image=self.bg_img, highlightthickness=0)
        wall_paper.place(x=0, y=0)

        # Creating four buttons for academicFrame, HobbyFrame, PgFrame, SkillFrame
        x = [100, 100, 100, 100]
        y = [200, 321, 442, 563]
        i = 0
        for F in ("Examination", "Competition", "CCA"):
            im = Image.open(pic_cwd + F + "Button.png")
            self.button_image = ImageTk.PhotoImage(im)
            self.button = tk.Button(self, image=self.button_image, borderwidth=0, highlightthickness=0,
                                    background="white",
                                    command=lambda cf=F: view_image(self, cf))
            self.button_change = ImageTk.PhotoImage(Image.open(pic_cwd + F + "Change.png"))
            change_on_hover(self.button, self.button_image, self.button_change)
            self.button.place(x=x[i], y=y[i])
            i += 1

        ret_button = tk.Button(self, text="return", command=lambda: controller.show_frame(MenuFrame))
        ret_button.place(x=0, y=0)


def view_image(frame, name):
    view = ImageViewer(frame, name)
    view.propagate(0)
    print(view.winfo_width())
    view.place(x=1440-1000., y=0)


class ImageViewer(tk.Frame):
    def __init__(self, parent, name):
        tk.Frame.__init__(self, parent, width=1000, height=900, borderwidth=0, highlightthickness=0, background="thistle")
        self.images = []
        i = 0
        # Store corresponding images
        while Path(pic_cwd + name + str(i) + ".png").is_file():
            self.images.append(ImageTk.PhotoImage(file=pic_cwd + name + str(i) + ".png"))
            i += 1

        # create global variable for display
        self.index = 0

        # Display first image
        self.img = self.images[self.index]
        self.cur_image = tk.Label(self, image=self.img, borderwidth=0, highlightthickness=0)
        self.cur_image.place(x=str(int(1000-self.images[self.index].width())/2), y=2)

        # Create buttons for left arrow and right arrow
        self.button_img_left_active = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonLeftActive.png").convert("RGBA"))
        self.button_img_right_active = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonRightActive.png").convert("RGBA"))
        self.button_img_left_disable = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonLeftDisable.png").convert("RGBA"))
        self.button_img_right_disable = ImageTk.PhotoImage(Image.open(pic_cwd+"buttonRightDisable.png").convert("RGBA"))
        if self.index == (len(self.images)-1):
            self.button_right = tk.Button(self, image=self.button_img_right_disable, background="thistle", borderwidth=0, command=lambda: self.display_right()
                                          , highlightthickness=0, state="disabled")
        else:
            self.button_right = tk.Button(self, image=self.button_img_right_active, background="thistle", borderwidth=0, command=lambda: self.display_right()
                                          , highlightthickness=0, state="normal")
        self.button_left = tk.Button(self, image=self.button_img_left_disable, background="thistle", borderwidth=0, command=lambda: self.display_left()
                                     , highlightthickness=0, state="disabled")
        self.button_left.place(x=(1000/2-15-113), y=700)
        self.button_right.place(x=(1000/2+15), y=700)

    def display_right(self):
        self.index += 1
        if self.index == len(self.images)-1:
            self.button_right.configure(state="disabled", image=self.button_img_right_disable)
        self.cur_image.configure(image=self.images[self.index])
        self.button_left.configure(state="normal", image=self.button_img_left_active)
        self.cur_image.place(x=str(int(1000 - self.images[self.index].width()) / 2), y=2)

    def display_left(self):
        self.index -= 1
        if self.index == 0:
            self.button_left.configure(state="disabled", image=self.button_img_left_disable)
        self.cur_image.configure(image=self.images[self.index])
        self.button_right.configure(state="normal", image=self.button_img_right_active)
        self.cur_image.place(x=str(int(1000 - self.images[self.index].width()) / 2), y=2)


class HobbyFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ret_button = tk.Button(self, text="return", command=lambda:controller.show_frame(MenuFrame))
        ret_button.place(x=0, y=0)


class PgFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ret_button = tk.Button(self, text="return", command=lambda:controller.show_frame(MenuFrame))
        ret_button.place(x=0, y=0)


class SkillFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ret_button = tk.Button(self, text="return", command=lambda:controller.show_frame(MenuFrame))
        ret_button.place(x=0, y=0)


app = Centre()
app.mainloop()
