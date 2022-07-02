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

lbl2 = Label(window, text="Обнаружить дефекты:", pady=5)
lbl2.grid(column=0, row=2)
btn2 = Checkbutton(window, text="Испорченное изображение")
btn2.grid(column=0, row=3)
btn3 = Checkbutton(window, text="Пропуск и повтор кадра")
btn3.grid(column=0, row=4)

chvar = IntVar()  # переменная выбора метода нумерации
chvar.set(0)
lbl5 = Label(window, text="Нумерация:")
lbl5.grid(column=0, row=5)
ch1 = Radiobutton(window, text="QR-коды", value=0, variable=chvar)
ch1.grid(column=0, row=6)
ch2 = Radiobutton(window, text="Фигуры", value=1, variable=chvar)
ch2.grid(column=1, row=6)

btn4 = Button(window, text="Начать", command= lambda : mydetector.detectDefect(chvar.get()))
btn4.grid(column=0, row=7, pady=10)

window.mainloop()
