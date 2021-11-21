#from tkinter import * 
import tkinter as tk 
import tkinter.messagebox as tkmb
import os 
from skimage import io   
from PIL import ImageTk
from PIL import Image

class Sorter:

    def __init__(self, buttons=['qq', 'pine']):
        
        self.root = tk.Tk()  
        self.current_image_data = None   

        # Preparing data loading 
        self.filenames = ['temp/input/'+x for x in os.listdir("temp/input/") if ".png" in x]
        self.imgs = [Image.open(x) for x in self.filenames]
        self.ioimgs= [io.imread(x) for x in self.filenames]
        self.generator = self.image_generator()

        self.canvas = tk.Canvas(self.root, width = 600, height = 600)      
        self.canvas.pack()         

        self.current_image_data = next(self.generator)
        self.item_container = self.canvas.create_image(20,20, anchor=tk.NW, image=self.current_image_data[1])      



        # Buttons 
        B = tk.Button(self.root, text ="Skip", command = self.nextImage)
        B.pack()

        for bstr in buttons:
            print(bstr)
            Q = tk.Button(self.root, text = bstr, command=lambda x=bstr: self.store(x))
            Q.pack(expand="YES")



        tk.mainloop() 

    # Image generator class 
    def image_generator(self):
        for i in range(len(self.filenames)):
            image = self.imgs[i]
            resize_image = image.resize((500, 500))
            img = ImageTk.PhotoImage(resize_image)
            yield self.filenames[i], img, self.ioimgs[i]

    def nextImage(self):
        self.current_image_data = next(self.generator)
        self.canvas.itemconfig(self.item_container, image=self.current_image_data[1]) # chaning image 

    def store(self, d):
        io.imsave(self.current_image_data[0].replace('input',d), arr=self.current_image_data[2])
        self.nextImage()


sorter = Sorter()