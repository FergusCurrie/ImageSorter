#from tkinter import * 
import tkinter as tk 
import tkinter.messagebox as tkmb
import os 
from skimage import io   
from PIL import ImageTk
from PIL import Image

class Sorter:

    def __init__(self, buttons=[]):
        self.imgsize = 500
        self.imgdir = 'temp/input/image/'
        self.buttons = buttons
        self.root = tk.Tk()  
        self.current_fns = None   

        self.filenames = [self.imgdir+x for x in os.listdir(self.imgdir) if ".png" in x]
        
        self.generator = self.image_generator()

        self.prepare_canvas()
        tk.mainloop() 
    
    def prepare_canvas(self):
         # Setup canvas
        self.canvas = tk.Canvas(self.root, width = 1200, height = 600)      
        self.current_fns = next(self.generator)
        self.nextImage()
        self.item_container_image = self.canvas.create_image(0,20, anchor=tk.NW, image=self.img_img)   # img    
        self.item_container_overlay = self.canvas.create_image(1200,20, anchor=tk.NE, image=self.img_ove) # overlay
        self.canvas.pack()  

        # Buttons 
        B = tk.Button(self.root, text ="Skip", command=lambda x='skip': self.store('skip'))
        B.pack()
        for bstr in self.buttons:
            Q = tk.Button(self.root, text = bstr, command=lambda x=bstr: self.store(x))
            Q.pack(expand="YES")

    def fn_to_data(self, fn):
        image = Image.open(fn)
        resize_image = image.resize((self.imgsize, self.imgsize))
        img = ImageTk.PhotoImage(resize_image)
        return img, io.imread(fn)
    
    # Image generator class 
    def image_generator(self):
        """
        Returns:
            filename, overlayfilename, maskfilename
        """
        for i in range(len(self.filenames)):
            fn = self.filenames[i]
            if not self.check_unsorted_fn(fn):
                continue
            ofn = fn.replace('image','overlay')
            mfn = fn.replace('image','mask') 
            yield fn, ofn, mfn

    def check_unsorted_fn(self,fn):
        """
        Check the given filename hasn't yet been sorted into another directory, this stops duplicates if program restarted. 
        """
        fn = fn.split('/')[2]
        for _fn in os.listdir('temp/skip/'):
            if fn == _fn:
                return False

        sorted_fns = []
        for d in os.listdir('temp/sorted'):
            if not d in ['.DS_Store', 'image', 'mask', 'overlay']:
                for p in os.listdir('temp/sorted/'+d):
                    for _fn in os.listdir(f'temp/sorted/{d}/{p}'):
                        sorted_fns.append(_fn)
        if fn in sorted_fns:
            return False
        else:
            return True

    def nextImage(self):
        """
        Pull next image from generator, return the ones to be drawn
        """
        self.current_fns = next(self.generator)
        self.img_img, _ = self.fn_to_data(self.current_fns[0])
        self.img_ove, _ = self.fn_to_data(self.current_fns[1])

    def drawImage(self):
        """
        Redraw the images 
        """
        self.nextImage()
        self.canvas.itemconfig(self.item_container_image, image=self.img_img) # chaning image 
        self.canvas.itemconfig(self.item_container_overlay, image=self.img_ove) # chaning image 

    def store(self, d):

        if d == 'skip':
            sfn = self.current_fns[0].split('/')[-1]
            _, ioimg = self.fn_to_data(self.current_fns[0])
            io.imsave('temp/skip/'+sfn, arr=ioimg)
        else:
            l = self.current_fns[0].replace('temp/input/','')
            path_fn = f'temp/sorted/{d}/{l}'
            print(path_fn)
            path = path_fn.split('/')[0] + '/' + path_fn.split('/')[1] + '/' + path_fn.split('/')[2] # just path
            if not os.path.isdir(path):
                os.mkdir(path)
                os.mkdir(path+'/image')
                os.mkdir(path+'/mask')

            # Save iamge 
            _, ioimg = self.fn_to_data(self.current_fns[0])
            _, iomsk = self.fn_to_data(self.current_fns[2])

            io.imsave(path_fn, arr=ioimg)
            io.imsave(path_fn.replace('image','mask'), arr=iomsk)
        self.drawImage()



categories = ["pine", "gorse", "shrub", "perfect"]
sorter = Sorter(categories)