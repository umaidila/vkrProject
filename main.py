from math import sqrt
from time import sleep
from tkinter import *
import cv2
import numpy as np


def showVideo():

    scr_diag = int(txt1.get())
    scr_width = int(txt2.get())
    scr_height = int(txt3.get())

    black_cell = cv2.imread('black_cell.jpg')
    white_cell = cv2.imread('white_cell.jpg')

    window = cv2.imread('girl.jpg')
    window = cv2.resize(window, (scr_width, scr_height))  # как фон

    diag_pix = sqrt(scr_width ** 2 + scr_height ** 2)  # диагональ в пикселях
    side = int(diag_pix / scr_diag)  # сторона клетки в пикселях (по идее 1 дюйм)

    isBlackStart = False  # тоже переключатель, задающий цвет в начале каждой строки
    x = 0
    y = 0  # бегунки заполняющие поле
    xArray = np.arange(0, scr_width, side)
    yArray = np.arange(0, scr_height, side)  # координаты шахматной сетки по x и y

    black_cell = cv2.resize(black_cell, (side, side))
    white_cell = cv2.resize(white_cell, (side, side))

    for i in range(len(yArray) - 1):
        isBlackStart = not isBlackStart
        isBlack = isBlackStart
        for j in range(len(xArray)):
            if j == len(xArray) - 1:  # если последняя клетка, то она будет обрезанной, нужно сначала изменить размер

                if isBlack:
                    black_cell = cv2.resize(black_cell, (scr_width - xArray[j], side))
                    window[yArray[i]:yArray[i + 1], xArray[j]:scr_width] = black_cell
                    black_cell = cv2.resize(black_cell, (side, side))  # и обратно
                else:
                    white_cell = cv2.resize(white_cell, (scr_width - xArray[j], side))
                    window[yArray[i]:yArray[i + 1], xArray[j]:scr_width] = white_cell
                    white_cell = cv2.resize(white_cell, (side, side))
            else:
                if isBlack:
                    window[yArray[i]:yArray[i + 1], xArray[j]:xArray[j + 1]] = black_cell
                    isBlack = False
                else:
                    window[yArray[i]:yArray[i + 1], xArray[j]:xArray[j + 1]] = white_cell
                    isBlack = True

    black_cell = cv2.resize(black_cell, (side, scr_height - yArray[len(yArray) - 1]))
    white_cell = cv2.resize(white_cell, (side, scr_height - yArray[len(yArray) - 1]))
    for i in range(len(xArray) - 1):  # заполение нижнего столбца
        isBlackStart = not isBlackStart
        if isBlackStart:
            window[yArray[len(yArray) - 1]:scr_height, xArray[i]:xArray[i + 1]] = black_cell
        else:
            window[yArray[len(yArray) - 1]:scr_height, xArray[i]:xArray[i + 1]] = white_cell

    isBlackStart = not isBlackStart
    # и последнюю клетку в углу:
    if isBlackStart:
        black_cell = cv2.resize(black_cell, (scr_width - xArray[len(xArray) - 1], scr_height - yArray[len(yArray) - 1]))
        window[yArray[len(yArray) - 1]:scr_height, xArray[len(xArray) - 1]:scr_width] = black_cell
    else:
        white_cell = cv2.resize(white_cell, (scr_width - xArray[len(xArray) - 1], scr_height - yArray[len(yArray) - 1]))
        window[yArray[len(yArray) - 1]:scr_height, xArray[len(xArray) - 1]:scr_width] = white_cell

    cv2.imshow('program', window)
    cv2.waitKey(0)



window = Tk()
window.title("hello world")
window.geometry('300x150')

lbl1 = Label(window,text="Диагональ монитора (дюйм): ",padx=20,pady=5)
lbl1.grid(column=0,row=0)
lbl2 = Label(window,text="Ширина монитора (пикс): ",pady=5)
lbl2.grid(column=0,row=1)
lbl3 = Label(window, text = "Высота монитора (пикс): ",pady=5)
lbl3.grid(column=0,row=2)

var1 = IntVar()
var1.set(21) # диагональ по умолчанию
var2 = IntVar()
var2.set(1024)
var3 = IntVar()
var3.set(768)

txt1 = Spinbox(window,from_=17,to=40,width=7,textvariable=var1)
txt1.grid(column=1,row=0)

txt2 = Entry(window,width=8,textvariable=var2)
txt2.grid(column=1,row=1)
txt3 = Entry(window,width=8,textvariable=var3)
txt3.grid(column=1,row=2)

startButton = Button(window,text="Начать",command=showVideo,pady=2)
startButton.grid(column=0,row=3)
window.mainloop()

