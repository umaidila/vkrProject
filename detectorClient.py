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



def getPathSource():
    mydetector.videoSource = askopenfilename()
    lbl1.config(text="Исходный видеофайл(выбран): ")


def getPathTest():
    mydetector.videoTest = askopenfilename()
    lbl6.config(text="Отснятый видеофайл(выбран):")


lbl1 = Label(window, text="Исходный видеофайл: ", padx=20, pady=10)
lbl1.grid(column=0, row=0)
btn1 = Button(window, text="Выбрать", command=getPathSource)
btn1.grid(column=1, row=0, padx=15)

lbl6 = Label(window, text="Отснятый видеофайл: ", padx=20, pady=10)
lbl6.grid(column=0, row=1)
btn5 = Button(window, text="Выбрать", command=getPathTest)
btn5.grid(column=1, row=1, padx=15)


btn4 = Button(window, text="Начать", command=mydetector.detectDefect)
btn4.grid(column=0, row=2, pady=10)

window.mainloop()
