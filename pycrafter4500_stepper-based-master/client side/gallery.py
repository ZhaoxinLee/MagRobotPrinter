from itertools import cycle
import tkinter as tk
from PIL import Image, ImageTk
import io
import os
import time
import pycrafter4500
from motormanager import MotorManager

# client = Client()
# mm = MotorManager(client)

class Gallery(tk.Tk):
    '''Tk window/label adjusts to size of image'''

    def __init__(self, img_title, list, time_ms, intensity, path, passes, mm):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(0)
        self.geometry("%dx%d+0+0" % (w, h))
        self.resizable(True, True)
        self.bind("<Escape>", lambda event:self.destroy())

        self.mm = mm
        self.image_title = img_title
        self.list = list
        self.time_ms = time_ms
        self.intensity = intensity
        self.path = path
        self.image_files = []
        self.delay = []
        self.img_name = None
        self.passes = passes
        self.field_phi = []
        self.field_theta = []
        for i in range(len(self.list)):
            if self.list[i][0] != '' and self.list[i][1] != '':
                self.image_files.append(self.image_title+str(list[i][0])+'.png')
                self.delay.append(list[i][1])
            if self.list[i][2] != '':
                self.field_phi.append(list[i][2])
            if self.list[i][3] != '':
                self.field_theta.append(list[i][3])

        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        self.pictures = cycle((self.photo_image(self.image_files[i]), self.image_files[i], self.delay[i]) for i in range(len(self.image_files)))
        self.picture_display = tk.Label(self)
        self.picture_display.pack()

        self.field = cycle((self.field_phi[i],self.field_theta[i]) for i in range(len(self.field_phi)))

    def run_field(self):
        phi, theta = next(self.field)
        for i in range(self.passes):
            if self.img_name != None and self.img_name != self.image_files[0]:
                self.cure(self.time_ms)
                if i != self.passes-1:
                    time.sleep(3)
        if self.img_name != None:
            self.mm.magneticFieldGo(phi,theta)
        self.after(1,self.show_slides)

    def show_slides(self):
        '''cycle through the images and show them'''

        # next works with Python26 or higher
        img_object, img_name, img_delay = next(self.pictures)
        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image
        self.img_name = img_name
        self.title(img_name)
        self.after(img_delay, self.run_field)


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
