import os
import tkinter
from math import sqrt
from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np
import qrcode

import detector

mydetector = detector.Detector()

window = Tk()
window.title("vkr")


def getPath():
    mydetector.videoTest = askopenfilename()
    print(mydetector.videoTest)


lbl1 = Label(window, text="Выберите видеофайл: ", padx=20, pady=10)
lbl1.grid(column=0, row=0)
btn1 = Button(window,text="Выбрать",command=getPath)
btn1.grid(column=1,row=0,padx=15)
lbl2 = Label(window,text="Обнаружить дефекты:",pady=5)
lbl2.grid(column=0,row=1)
btn2 = Checkbutton(window,text="Испорченное изображение")
btn2.grid(column=0,row=2)
btn3 = Checkbutton(window,text="Пропуск и повтор кадра")
btn3.grid(column=0,row=3)
lbl3 = Label(window,text="FPS видео:")
lbl3.grid(column=0,row=4)

var1 = IntVar()
var1.set(30)

txt1 = Spinbox(window, from_=5, to=120, width=7, textvariable=var1)
txt1.grid(column=1, row=4)

chvar = IntVar()  # переменная выбора метода нумерации
chvar.set(0)
lbl5 = Label(window,text="Нумерация:")
lbl5.grid(column=0,row=5)
ch1 = Radiobutton(window, text="QR-коды", value=0, variable=chvar)
ch1.grid(column=0, row=6)
ch2 = Radiobutton(window, text="Фигуры", value=1, variable=chvar)
ch2.grid(column=1, row=6)

lbl4 = Label(window,text="Выберите файл вывода")
lbl4.grid(column=0,row=7)
btn4 = Button(window,text="Выбрать",command=mydetector.detectDefect)
btn4.grid(column=1,row=7,pady=10)

window.mainloop()