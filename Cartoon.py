import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import cv2


top=tk.Tk()
top.geometry('1000x600')
top.title('Avatar--Make Your Own')

top.configure(background='white')


MainFrame = Frame(top)
MainFrame.grid()

#Title Frame
TitleFrame = Frame(MainFrame, width=650, bd=10, relief=RIDGE)
TitleFrame.pack(side=TOP)
        
lb1Title = Label(TitleFrame, width=59, font=('Times New Roman', 20, 'bold'),text="Create Your Own Avatar\t", bg="cadetblue",fg='crimson', padx=14)
lb1Title.grid()



#Side Frame
SideFrame = Frame(MainFrame, width=500, bd=10,relief=RIDGE)
SideFrame.pack(side=TOP)

#Side Frame Left
DataFrameLeft = LabelFrame(SideFrame, bd=7, width=250, height=518 , padx=14, relief=RIDGE, font=('Times New Roman',12,'bold'), text="Photo:", fg="cadetblue")
DataFrameLeft.pack(side=LEFT)


#Side Frame Right
DataFrameRight = LabelFrame(SideFrame, bd=7, width=720, height=518, padx=14, relief=RIDGE, font=('Times New Roman',12,'bold'), text="Result:", fg="cadetblue")
DataFrameRight.pack(side=RIGHT)


#Filters Name Attach to Left Side Frame
lb1Filter = Label(DataFrameLeft, font=('Times New Roman', 12), text="Filters:", padx=2, pady=2)
lb1Filter.grid(row=1, column=0, sticky=W)
cbFilter = Combobox(DataFrameLeft, state='readonly', font=('Times New Roman', 10), width=15)
cbFilter['value'] = ('--select--', 'Pencil Sketch', 'Detail Enhancement', 'Avatar', 'Pencil Edges')
cbFilter.current(0)

cbFilter.grid(row=1, column=1)

#Saving Image after applying filters
def save_cartoon(file_path,cartoon_img):
    where=filedialog.asksaveasfilename(filetypes=(('JPEG Files','*.jpg'),('PNG Files','*.png'),('All Files','*.*')),defaultextension=file_path[-4:])
    cartoon_img.save(where)

#Showing Save Button
def show_save_button(file_path,cartoon_img):
    save_b=Button(DataFrameLeft,text='Save to computer', command=lambda: save_cartoon(file_path,cartoon_img),padx=10,pady=5)
    #save_b.place(relx=0.69,rely=0.86)
    save_b.grid(row=3, column=0,sticky=W)


#Convert Function
def convert(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #convert the image into grayscale image

    if(cbFilter.get()=="Detail Enhancement"):
                                        #Blur the grayscale image with median blur
        gray_blur = cv2.medianBlur(gray, 3) 
                                        #Apply adaptive thresholding to detect edges
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9) 
                                        #Sharpen the image
        color = cv2.detailEnhance(img, sigma_s=5, sigma_r=0.5)
                                        #Merge the colors of same images using "edges" as a mask
        cartoon = cv2.bitwise_and(color, color, mask=edges)
    elif(cbFilter.get()=="Pencil Sketch"):
                                        # Blur the image using Gaussian Blur
        gray_blur = cv2.GaussianBlur(gray, (165, 165), 50)
                                        # Convert the image into pencil sketch
        cartoon = cv2.divide(gray, gray_blur, scale=260.0)
    
    elif(cbFilter.get()=="Pencil Edges"):
                                        # Blur the image using Gaussian Blur
        gray_blur = cv2.GaussianBlur(gray, (25, 25), 0, 0)
                                        # Convert the image into pencil sketch
        cartoon = cv2.divide(gray, gray_blur, scale=260.0)

    elif(cbFilter.get()=="Avatar"):
        gray = cv2.medianBlur(gray, 5) 
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 250, 250) 
        cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    cartoon=cv2.cvtColor(cartoon,cv2.COLOR_BGR2RGB)
    cartoon_img=Image.fromarray(cartoon)
    cartoon_img.thumbnail(((top.winfo_width()/2),(top.winfo_height()/2)))
    im=ImageTk.PhotoImage(cartoon_img)
    label=Label(DataFrameRight,image=im)
    label.image=im
    label.grid(row=2, column=1,sticky=W)
    show_save_button(file_path,cartoon_img)
    
    



#Show convert button
def show_convert_button(file_path):
    convert_b=Button(DataFrameLeft,text="Apply Changes",command=lambda: convert(file_path),padx=10,pady=5)
    #convert_b.place(relx=0.79,rely=0.46)
    convert_b.grid(row=3, column=1,sticky=W)


#Image Upload function
def upload_image():
    file_path=filedialog.askopenfilename()
    uploaded=Image.open(file_path)
    uploaded.thumbnail(((top.winfo_width()/3),(top.winfo_height()/3)))
    im=ImageTk.PhotoImage(uploaded)
    label=Label(DataFrameLeft,image=im)
    label.image=im
    label.grid(row=5,column=0,sticky=S)
    show_convert_button(file_path)

#Image Upload Button Linked to Upload function
upload=Button(DataFrameLeft,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#adadee', foreground='white',font=('arial',10,'bold'))
upload.grid(row=0, column=1,sticky=W)

top.mainloop()