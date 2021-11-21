#from tkinter import * 
import tkinter as tk 
import tkinter.messagebox as tkmb
import os 
from skimage import io   
from PIL import ImageTk
from PIL import Image

class Sorter:

    def __init__(self, buttons=[]):

        self.root = tk.Tk()  
        self.current_image_data = None   

        # Preparing data loading 
        self.filenames = ['temp/input/'+x for x in os.listdir("temp/input/") if ".png" in x]
        self.imgs = [Image.open(x) for x in self.filenames]
        self.ioimgs= [io.imread(x) for x in self.filenames]
        self.generator = self.image_generator()

        # Setup canvas
        self.canvas = tk.Canvas(self.root, width = 600, height = 600)      
        self.canvas.pack()         
        self.current_image_data = next(self.generator)
        self.item_container = self.canvas.create_image(20,20, anchor=tk.NW, image=self.current_image_data[1])      



        # Buttons 
        B = tk.Button(self.root, text ="Skip", command=lambda x=bstr: self.store('skip'))
        B.pack()
        for bstr in buttons:
            Q = tk.Button(self.root, text = bstr, command=lambda x=bstr: self.store(x))
            Q.pack(expand="YES")
        tk.mainloop() 


    # Image generator class 
    def image_generator(self):
        for i in range(len(self.filenames)):
            fn = self.filenames[i]
            if not self.check_unsorted_fn(fn):
                print('sorted')
                continue
            print('unsroted')

            image = Image.open(fn)
            resize_image = image.resize((500, 500))
            img = ImageTk.PhotoImage(resize_image)
            yield self.filenames[i], img, io.imread(fn)

    def check_unsorted_fn(self,fn):
        fn = fn.split('/')[2]
        sorted_fns = []
        for d in os.listdir('temp'):
            if d != 'input' and d != '.DS_Store':
                for _fn in os.listdir('temp/'+d):
                    sorted_fns.append(_fn)

        print(sorted_fns)
        if fn in sorted_fns:
            return False
        else:
            return True

    def nextImage(self):
        self.current_image_data = next(self.generator)
        self.canvas.itemconfig(self.item_container, image=self.current_image_data[1]) # chaning image 

    def store(self, d):
        path_fn = self.current_image_data[0].replace('input',d) # temp/gorse/image.17_129849_80778.png
        path = path_fn.split('/')[0] + '/' + path_fn.split('/')[1]
        if not os.path.isdir(path):
            os.mkdir(path)
        io.imsave(path_fn, arr=self.current_image_data[2])
        self.nextImage()



categories = ["pine", "gorse", "shrub", "perfect"]
sorter = Sorter(categories)