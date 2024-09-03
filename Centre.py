import tkinter as tk
import sys
from PIL import Image, ImageTk
import ctypes
import webbrowser

pic_cwd = sys.path[0] + "\\pic\\"
ctypes.windll.shcore.SetProcessDpiAwareness(1)
poppler_bin = sys.path[0]+"\\poppler-24.07.0\\"+"Library\\"+"bin"


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
        i = 0
        x = [[505, 735, 500, 735], [100, 100, 100, 100], [100, 100, 100, 100], [100, 100, 100, 100], [100, 100, 100, 100]]
        y = [[440, 440, 600, 600], [300, 421, 542, 663], [300, 421, 542, 663], [300, 421, 542, 663], [300, 421, 542, 663]]
        pic_names = [["AcademicFrame", "PgFrame", "SkillFrame", "HobbyFrame"], ["Examination", "Competition", "CCA"],
                     ["Exercise"], ["Language", "Office"], ["CS61B", "CS144", "MIT6828", "LeetCode"]]
        # funcs = [self.show_frame, NewFrame.view_image, NewFrame.view_image,
        #          NewFrame.view_image, NewFrame.view_image]
        # for f in ("MenuFrame", "AcademicFrame", "HobbyFrame", "PgFrame", "SkillFrame"):
        for f in ("MenuFrame", "AcademicFrame", "HobbyFrame"):
            name = f
            frame = NewFrame(container, self, name, x[i], y[i], pic_names[i])
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            i += 1
        self.show_frame("MenuFrame")

    def show_frame(self, name):
        change_frame = self.frames[name]
        change_frame.tkraise()


def change_on_hover(canvas, button, image_leave, image_enter, func, *var):
    canvas.tag_bind(button, '<Enter>', lambda x: canvas.itemconfig(button, image=image_enter))
    canvas.tag_bind(button, '<Leave>', lambda x: canvas.itemconfig(button, image=image_leave))
    if len(var) == 0:
        canvas.tag_bind(button, '<Button-1>', lambda x: func())
    else:
        canvas.tag_bind(button, '<Button-1>', lambda x: func(var[0]))


class NewFrame(tk.Frame):
    def __init__(self, parent, controller, name, x, y, pic_names):
        tk.Frame.__init__(self, parent)
        self.cwd = pic_cwd+name+"\\"
        self.canvas = tk.Canvas(self, width=1440, height=900, bg="red")
        self.canvas.pack()

        # Adding background image
        self.img = Image.open(self.cwd + "Bg.jpg")  # ok
        self.bg_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

        if name != "MenuFrame":
            self.ret_img = ImageTk.PhotoImage(Image.open(self.cwd + "ret.png"))
            self.ret_change_img = ImageTk.PhotoImage(Image.open(self.cwd + "retChange.png"))
            button = self.canvas.create_image(3, 3, image=self.ret_img, anchor='nw')
            change_on_hover(self.canvas, button, self.ret_img, self.ret_change_img, self.ret_menu, controller)

        # Initializing the buttons
        # func = self.view_image
        self.img_viewers = {}
        func = self.show_frame
        if name == "MenuFrame":
            func = controller.show_frame
        i = 0
        for n in pic_names:
            cn = n
            cur_cwd = self.cwd+cn+"\\"
            if name != "MenuFrame":
                viewer = ImageViewer(self.canvas, cn, self.cwd)
                self.img_viewers[n] = viewer
                # viewer.grid(row=0, column=0, sticky="nsew")
            self.button_image = ImageTk.PhotoImage(Image.open(cur_cwd + "Button.png"))
            self.button_change = ImageTk.PhotoImage(Image.open(cur_cwd + "Change.png"))
            self.button = self.canvas.create_image(x[i], y[i], image=self.button_image, anchor='nw')
            change_on_hover(self.canvas, self.button, self.button_image, self.button_change,
                            func, cn)
            i += 1
        self.cur_img_viewer = None

    def ret_menu(self, controller):
        self.cur_img_viewer.place_forget()
        controller.show_frame("MenuFrame")


    def show_frame(self, name):
        if self.cur_img_viewer is not None:
            self.cur_img_viewer.place_forget()
        self.cur_img_viewer = self.img_viewers[name]
        self.cur_img_viewer.propagate(0)
        self.cur_img_viewer.place(x=1440 - 1000, y=0)
        

    # This method is to call an ImageViewer object
    # def view_image(self, *var):
    #     if self.img_viewer is not None:
    #         self.img_viewer.destroy()
    #     cur_vars = list(var)
    #     self.img_viewer = ImageViewer(self, cur_vars[0], cur_vars[1])
    #     self.img_viewer.propagate(0)
    #     self.img_viewer.place(x=1440 - 1000, y=0)


class ImageViewer(tk.Frame):
    def __init__(self, parent, name, cwd):
        tk.Frame.__init__(self, parent, width=1000, height=900, borderwidth=0, highlightthickness=0)

        button_cwd = pic_cwd+"ImageViewer//"
        # Create buttons for left arrow and right arrow
        self.button_img_left_active = ImageTk.PhotoImage(Image.open(button_cwd + "buttonLeftActive.png"))
        self.button_img_right_active = ImageTk.PhotoImage(Image.open(button_cwd + "buttonRightActive.png"))
        self.button_img_left_disable = ImageTk.PhotoImage(Image.open(button_cwd + "buttonLeftDisable.png"))
        self.button_img_right_disable = ImageTk.PhotoImage(Image.open(button_cwd + "buttonRightDisable.png"))
        self.button_img_left_change = ImageTk.PhotoImage(Image.open(button_cwd + "buttonLeftChange.png"))
        self.button_img_right_change = ImageTk.PhotoImage(Image.open(button_cwd + "buttonRightChange.png"))

        # Store corresponding images
        cwd = cwd + name + "\\"

        # A method to get a image with name img+number of all types(pdf, jpg, png .etc)
        # def get_image(file_name):
        #     if Path(file_name + ".png").is_file():
        #         return ".png"
        #     if Path(file_name + ".jpg").is_file():
        #         return ".jpg"
        #     if Path(file_name + ".pdf").is_file():
        #         return ".pdf"
        #     if Path(file_name + ".gif").is_file():
        #         return ".gif"
        #     return ".none"
        file_list = open(cwd+"list.txt", "r").readlines()
        self.images = []
        self.images_types = []
        image_path = cwd+"img"+str(i)
        image_type = get_image(image_path)
        for file_name in file_list:
            if file_name[len(file_name)-2] == 'd':
                image_path = cwd + "img" + str(i)
                image_type = get_image(image_path)

        self.canvas = tk.Canvas(self, width=1440, height=900, background="thistle")
        self.canvas.pack(fill='both', expand=True)

        # create global variable for display
        self.index = -1

        # Initialize the left and right buttons
        self.button_right = self.canvas.create_image(1000 / 2 + 15, 700, image=self.button_img_right_active, anchor='nw')
        self.button_left = self.canvas.create_image(1000 / 2 - 15 - 113, 700, image=self.button_img_left_active, anchor='nw')
        change_on_hover(self.canvas, self.button_left, self.button_img_left_active,
                        self.button_img_left_change, self.display_left)
        change_on_hover(self.canvas, self.button_right, self.button_img_right_active,
                        self.button_img_right_change, self.display_right)
        self.button_right_disable = None
        self.button_left_disable = self.canvas.create_image(1000 / 2 - 15 - 113, 700, image=self.button_img_left_disable, anchor='nw')

        # Display first image
        self.img = Image.new('RGB', (100, 100))
        self.cur_image = self.canvas.create_image(1000/2, 60, image=ImageTk.PhotoImage(self.img), anchor='n')
        self.display_right()
        self.button_left_disable = self.canvas.create_image(1000 / 2 - 15 - 113, 700, image=self.button_img_left_disable, anchor='nw')
        # Display title of the image
        # self.cur_img_title = tk.Label(self.canvas, text="img"+str(self.index)+self.images_types[self.index],
        # background="cyan", font=('Arial', 14), foreground="black", borderwidth=2, highlightthickness=2, highlightbackground='black')
        # self.cur_img_title.place(x=1000/2, y=4, anchor='n')

        # Create a container for pdf_button
        self.pdf_button =



    def display_right(self):
        # If the previous file is pdf, forget it
        if self.pdf is not None:
            self.pdf.place_forget()
        self.index += 1
        # If this is the first picture or pdf, place a disable gray button so that the user cannot click the button
        if self.index == len(self.images)-1:
            self.button_right_disable = self.canvas.create_image(1000 / 2 + 15, 700,
                                                                image=self.button_img_right_disable, anchor='nw')
        # If the cur image is not a pdf, straightly show it
        if isinstance(self.images[self.index], ImageTk.PhotoImage):
            self.canvas.itemconfig(self.cur_image, image=self.images[self.index])
        else:

        # Since we already moved right, we can activate the move_left button
        self.canvas.delete(self.button_left_disable)

    def display_left(self):
        # If the previous file is pdf, forget it
        if self.pdf is not None:
            self.pdf.place_forget()
        self.index -= 1
        # If this is the first picture or pdf, place a disable gray button so that the user cannot click the button
        if self.index == 0:
            self.button_left_disable = self.canvas.create_image(1000 / 2 - 15 - 113, 700,
                                                                image=self.button_img_left_disable, anchor='nw')
        # If the cur image is not a pdf, straightly show it
        if isinstance(self.images[self.index], ImageTk.PhotoImage):
            self.canvas.itemconfig(self.cur_image, image=self.images[self.index])
        else:

        # Since we already moved right, we can activate the move_left button
        self.canvas.delete(self.button_right_disable)


# class PdfViewer(tk.Frame):
#     def __init__(self, parent, images):
#         tk.Frame.__init__(self, parent, width=1000, height=600)
#
#         # Store all pages in pdf as photoImage array
#         self.images = []
#         for image in images:
#             image = image.resize((image.width*600//image.height, 600))
#             self.images.append(ImageTk.PhotoImage(image))
#         # Create main canvas
#         self.canvas = tk.Canvas(self, width=1000, height=600, background="red")
#         self.canvas.pack(fill='x', expand=True)
#
#         # Get button images
#         pdfviewer_cwd = pic_cwd + "PDFViewer\\"
#         image_left_active = ImageTk.PhotoImage(Image.open(pdfviewer_cwd+"buttonLeftActive.png"))
#         image_right_active = ImageTk.PhotoImage(Image.open(pdfviewer_cwd + "buttonRightActive.png"))
#         image_left_change = ImageTk.PhotoImage(Image.open(pdfviewer_cwd + "buttonLeftChange.png"))
#         image_right_change = ImageTk.PhotoImage(Image.open(pdfviewer_cwd + "buttonRightChange.png"))
#         self.image_left_disable = ImageTk.PhotoImage(Image.open(pdfviewer_cwd + "buttonLeftDisable.png"))
#         self.image_right_disable = ImageTk.PhotoImage(Image.open(pdfviewer_cwd + "buttonRightDisable.png"))
#
#         # Put button images onto the canvas
#         self.x_button_left = 0+40
#         self.x_button_right = 1000-40-80
#         button_left = self.canvas.create_image(self.x_button_left, 600, image=image_left_active, anchor='nw')
#         button_right = self.canvas.create_image(self.x_button_right, 600, image=image_right_active, anchor='nw')
#         change_on_hover(self.canvas, button_left, image_left_active, image_left_change, self.move_left)
#         change_on_hover(self.canvas, button_right, image_right_active, image_right_change, self.move_right)
#         self.button_left_disable = self.canvas.create_image(self.x_button_left, 600, image=self.image_left_disable, anchor='nw')
#         self.button_right_disable = self.canvas.create_image(self.x_button_right, 600, image=self.image_right_disable, anchor='nw')
#         self.canvas.delete(self.button_right_disable)
#
#         # Display first image
#         self.index = -1
#         self.img = Image.new('RGB', (100, 100))
#         self.cur_image = self.canvas.create_image(0, 2, image=ImageTk.PhotoImage(self.img), anchor='nw')
#         self.move_right()
#         self.button_left_disable = self.canvas.create_image(self.x_button_left, 600, image=self.image_left_disable,
#                                                             anchor='nw')
#
#
#     def move_left(self):
#         if self.index == 0:
#             self.canvas.create_image(self.x_button_left, 600, image=self.image_left_disable, anchor='nw')
#         self.canvas.itemconfig(self.cur_image, image=self.images[self.index])
#         self.canvas.delete(self.button_right_disable)
#
#     def move_right(self):
#         if self.index == (len(self.images)-1):
#             self.canvas.create_image(self.x_button_left, 600, image=self.image_left_disable, anchor='nw')
#         self.canvas.itemconfig(self.cur_image, image=self.images[self.index])
#         self.canvas.delete(self.button_left_disable)








app = Centre()
app.mainloop()
