import os
from math import sqrt
from tkinter import *
import cv2
import numpy as np
import qrcode


window = Tk()
window.title("vkr")
#window.geometry('300x210')

lbl1 = Label(window, text="Выберите видеофайл: ", padx=20, pady=10)
lbl1.grid(column=0, row=0)
btn1 = Button(window,text="Выбрать")
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
btn4 = Button(window,text="Выбрать")
btn4.grid(column=1,row=7,pady=10)
'''

lbl2 = Label(window, text="Ширина монитора (пикс): ", pady=5)
lbl2.grid(column=0, row=1)
lbl3 = Label(window, text="Высота монитора (пикс): ", pady=5)
lbl3.grid(column=0, row=2)
lbl4 = Label(window, text="Кадров в секунду:", pady=5)
lbl4.grid(column=0, row=3)
lbl5 = Label(window, text="Длительность (сек): ", pady=5)
lbl5.grid(column=0, row=4)

lbl6 = Label(window)
lbl6.grid(column=1, row=6)  # инфополе для вывода инфы что всё готово при завершении

chvar = IntVar()  # переменная выбора метода нумерации
chvar.set(0)
ch1 = Radiobutton(window, text="QR-коды", value=0, variable=chvar)
ch1.grid(column=0, row=5)
ch2 = Radiobutton(window, text="Фигуры", value=1, variable=chvar)
ch2.grid(column=1, row=5)

var1 = IntVar()
var1.set(21)  # диагональ по умолчанию
var2 = IntVar()
var2.set(1024)
var3 = IntVar()
var3.set(768)
var4 = IntVar()
var4.set(30)
var5 = IntVar()
var5.set(60)

txt1 = Spinbox(window, from_=17, to=40, width=7, textvariable=var1)
txt1.grid(column=1, row=0)
txt2 = Entry(window, width=8, textvariable=var2)
txt2.grid(column=1, row=1)
txt3 = Entry(window, width=8, textvariable=var3)
txt3.grid(column=1, row=2)
txt4 = Spinbox(window, from_=5, to=120, width=7, textvariable=var4)
txt4.grid(column=1, row=3)
txt5 = Entry(window, width=8, textvariable=var5)
txt5.grid(column=1, row=4)

'''

window.mainloop()