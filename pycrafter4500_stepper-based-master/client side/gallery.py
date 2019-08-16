from itertools import cycle
import tkinter as tk
from PIL import Image, ImageTk
import io
import os
import pycrafter4500

class Gallery(tk.Tk):
    '''Tk window/label adjusts to size of image'''

    def __init__(self, img_title, list, time_ms, intensity, path):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (w, h))
        self.resizable(False, False)
        self.bind("<Escape>", lambda event:self.destroy())

        self.image_title = img_title
        self.list = list
        self.time_ms = time_ms
        self.intensity = intensity
        self.path = path
        self.image_files = []
        self.delay = []
        for i in range(len(self.list)):
            if self.list[i] != []:
                self.image_files.append(self.image_title+str(list[i][0])+'.png')
                self.delay.append(list[i][1])
        # print(self.image_files)
        # print(self.delay)

        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        self.pictures = cycle((self.photo_image(self.image_files[i]), self.image_files[i], self.delay[i]) for i in range(len(self.image_files)))
        self.picture_display = tk.Label(self)
        self.picture_display.pack()

    def show_slides(self):
        '''cycle through the images and show them'''

        # next works with Python26 or higher
        img_object, img_name, img_delay = next(self.pictures)
        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image

        #self.cure(self.time_ms)
        self.title(img_name)
        self.after(img_delay, self.show_slides)


    def photo_image(self, jpg_filename):

        dir = os.path.dirname(self.path)
        filename = os.path.join(dir,jpg_filename)

        with io.open(filename, 'rb') as ifh:
            pil_image = Image.open(ifh)
            return ImageTk.PhotoImage(pil_image)

    def run(self):
        self.mainloop()

    def cure(self,time_ms):
        if time_ms == 0:
            intensity = 0xFF - self.intensity
            pycrafter4500.set_LED_current(intensity)
            time.sleep(0.01)
        else:
            pycrafter4500.set_LED_current(self.intensity)
            time.sleep(self.time_ms/1000)
            pycrafter4500.set_LED_current(255)
            time.sleep(10)


# get a series of gif images you have in the working folder
# or use full path, or set directory to where the images are
# image_files = [
# 'frog1.png',
# 'frog2.png',
# 'frog3.png',
# 'frog4.png'
# ]


# class Picture(tk.Tk):
#     def __init__(self, delay_time, x=None, y=None):
#         self.delay_time = delay_time
#         self.image = Image.open('frog99.png')
#         #print(image)
#         #self.image.show()
#
#         # the root will be self
#         tk.Tk.__init__(self)
#         # set x, y position only
#         w, h = self.winfo_screenwidth(), self.winfo_screenheight()
#         self.overrideredirect(0)
#         self.geometry("%dx%d+0+0" % (w, h))
#         self.resizable(False, False)
#         self.picture_display = tk.Label(self)
#         self.picture_display.pack()
#         img_object = ImageTk.PhotoImage(self.image)
#         self.picture_display.config(image=img_object)
#         # shows the image filename, but could be expanded
#         # to show an associated description of the image
#
#     def update_image(self,image_number,delay_time):
#         self.delay_time = delay_time
#         self.image_number = image_number
#         self.picture_display.destroy()
#         self.image = Image.open('frog{}.png'.format(self.image_number))
#         w, h = self.winfo_screenwidth(), self.winfo_screenheight()
#         self.overrideredirect(0)
#         self.geometry("%dx%d+0+0" % (w, h))
#         self.resizable(False, False)
#         self.picture_display = tk.Label(self)
#         self.picture_display.pack()
#         img_object = ImageTk.PhotoImage(self.image)
#         self.picture_display.config(image=img_object)
#         # shows the image filename, but could be expanded
#         # to show an associated description of the image
#         self.title('frog{}.png'.format(self.image_number))
#         self.mainloop()
#         self.after(self.delay_time, self.update_image)
