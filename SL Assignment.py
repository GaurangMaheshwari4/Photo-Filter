from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
import os

#Creating Folder for Captured images
def Image_folder():
    folder = r"/Photo Filter/"
    cwd = os.getcwd()
    global path 
    path = cwd+folder
    if not os.path.exists(path):
        os.makedirs(path)

# create a dictionary for the filters
filt = ['color', 'gray', 'gauss','delta','sobel', 'laplace', 'threshold', 'delta_plus', 'blue', 'sobelxy']
filter_sel = {}

def choose_filter(filter, status):
    # change required filter to true
    filter_sel = {x:False for x in filt}
    if filter in filter_sel:
        assert type(status) == bool
        filter_sel[filter] = status
    return filter_sel

class Welcome(Tk):
    def __init__(self):
        super().__init__()
        #self.resizable(0,0)
        self.title("Photo Filter")
        self.configure(background="SkyBlue1")
        self.vid = MyVideoCapture()

        # make dictionary for all filters and initialise color one as True
        self.all_filters = choose_filter('color', True)
        self.delta_plus_frame = None

        Label(self,text="Filters",font=("Helvetica",15),relief=FLAT,bg="SkyBlue1").grid(row=0,column=13, columnspan=5)

        #Canvas for video to appear
        self.canvas	= Canvas(self, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0, rowspan=15, columnspan=5)

        Button(self, text="Capture",font=("Helvetica",15),width=30,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.capture).grid(row=12, column=2, rowspan=7)

        Button(self, text="Gauss", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.gauss_filter).grid(row=1, column=13)

        Button(self, text="Laplace", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.laplace_filter).grid(row=1, column=17)

        Button(self, text="Delta", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.delta_filter).grid(row=3, column=13)

        Button(self, text="Delta+", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.delta_filter_plus).grid(row=3, column=17)

        Button(self, text="Threshold", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.threshold_filter).grid(row=5, column=13)

        Button(self, text="Sobel-x, xy", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.sobel_filter).grid(row=5, column=17)

        Button(self, text="Blue", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command = self.blue_filter).grid(row=7, column=13)

        Button(self, text="Gray", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.gray_filter).grid(row=7, column=17)

        Button(self, text="Normal", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.no_filter).grid(row=9, column=13)

        Button(self, text="Quit", font=("Helvetica",15),width=15,relief=SOLID,bg="SkyBlue1",activebackground="SkyBlue1",activeforeground="blue",command=self.destroy).grid(row=9, column=17)

        self.delay = 10
        self.update()

    def	capture(self):
        cv2.imwrite(path+r"Picture-"+time.strftime("%d-%m-%Y-%H-%M-%S")+'.jpg', self.frame)
    
    def	update(self):
        ret,frame, frame1=self.vid.get_frame()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        if self.all_filters['color']:
            pass
        elif self.all_filters['gray']:
            frame = gray
        elif self.all_filters['gauss']:
            frame = cv2.GaussianBlur(gray, (21,21), 0)
        elif self.all_filters['delta']:
            frame = cv2.absdiff(frame1, gray)
        elif self.all_filters['sobel']:
            frame = cv2.Sobel(gray,-1,  dx=1, dy=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        elif self.all_filters['sobelxy']:
            sobelx = cv2.Sobel(gray,-1,  dx=1, dy=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            sobely = cv2.Sobel(gray,-1,  dy=1, dx=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            frame = sobelx+sobely
        elif self.all_filters['laplace']:
            frame = cv2.Laplacian(gray, -1, ksize=17, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        elif self.all_filters['threshold']:
            frame = cv2.threshold(cv2.absdiff(frame1, gray), 30, 255, cv2.THRESH_BINARY)[1]
        elif self.all_filters['delta_plus']:
            if self.delta_plus_frame is None:
                self.delta_plus_frame = gray
            frame = cv2.absdiff(self.delta_plus_frame, gray)
        elif self.all_filters['blue']:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Update Image and show on the frame
        if	ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.photo=ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0,0,image=self.photo,anchor='nw')
        self.after(self.delay,self.update)

        self.frame = frame
    
    def gray_filter(self):
        self.all_filters = choose_filter('gray', True)
    def delta_filter_plus(self):
        self.delta_plus_frame = None
        self.all_filters = choose_filter('delta_plus', True)
    def gauss_filter(self):
        self.all_filters = choose_filter('gauss', True)
    def delta_filter(self):
        self.all_filters = choose_filter('delta', True)
    def laplace_filter(self):
        self.all_filters = choose_filter('laplace', True)
    def threshold_filter(self):
        self.all_filters = choose_filter('threshold', True)
    def sobel_filter(self):
        if self.all_filters['sobel'] == True:
            self.all_filters = choose_filter('sobelxy', True)
        else:
            self.all_filters = choose_filter('sobel', True)
    def no_filter(self):
        self.all_filters = choose_filter('color', True)
    def blue_filter(self):
        self.all_filters = choose_filter('blue', True)




class MyVideoCapture:
    def	__init__(self):
        self.vid=cv2.VideoCapture(0)
        if	not	self.vid.isOpened():
            print("Unable	to open	video source")
        
        self.width	= self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height	= self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame1 = None


    def	get_frame(self):
        if	self.vid.isOpened():
            ret, frame = self.vid.read()
            if self.frame1 is None:
                self.frame1= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret:
                return (ret, frame,  self.frame1)
            else:
                return (ret, None)
        else:
            return	(False, None)

    def	__del__(self):
        if	self.vid.isOpened():
            self.vid.release()





if __name__=="__main__":
    Image_folder()
    root = Welcome()
    root.mainloop()