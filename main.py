from math import sqrt
from tkinter import *
import cv2
import numpy as np
import qrcode


def showVideo():
    def shift(a, l):  # смещение массива по горизонтали, l - длина
        temp = a[:, 0]
        a[:, :l - 1] = a[:, 1:]
        a[:, l - 1] = temp
        return a

    lbl6.config(text="wait")

    scr_diag = int(txt1.get())
    scr_width = int(txt2.get())
    scr_height = int(txt3.get())
    duration = int(txt5.get())
    fps = int(txt4.get())
    '''
    qr1 = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr1.add_data(1)
    qr1.make(fit=True)

    img1 = qr1.make_image(fill='black', back_color='white')
    img1.save('temp1.png')
    img1 = cv2.imread('temp1.png')
    img1 = cv2.resize(img1, (200, 200))

    '''
    # fourcc = cv2.VideoWriter_fourcc(*'divx')
    out = cv2.VideoWriter('output.mp4', 0x00000021, int(txt4.get()), (scr_width, scr_height))

    black_cell = cv2.imread('black_cell.jpg')
    white_cell = cv2.imread('white_cell.jpg')

    temp = cv2.imread('black_cell.jpg')
    temp = cv2.resize(temp, (1, scr_height))

    diag_pix = sqrt(scr_width ** 2 + scr_height ** 2)  # диагональ в пикселях
    side = int(diag_pix / scr_diag)  # сторона клетки в пикселях (по идее 1 дюйм)

    isBlackStart = False  # переключатель, задающий цвет в начале каждой строки

    xArray = np.arange(0, scr_width, side)
    yArray = np.arange(0, scr_height, side)  # координаты шахматной сетки по x и y

    black_cell = cv2.resize(black_cell, (side, side))
    white_cell = cv2.resize(white_cell, (side, side))

    window = cv2.imread('girl.jpg')

    if len(xArray) % 2 != 0:  # колво клеток по горизонтали должно быть чётным, чтобы при сдвиге соседние клетки были разного цвета
        print('нечёт')
        window = cv2.resize(window, (
            (len(xArray)+1) * side,
            scr_height))  # расширяем окно по х, чтобы нарисовать обрезанные клетки
        xArray = np.arange(0, (len(xArray)+1) * side, side)
    else:
        print('чёт')
        window = cv2.resize(window, (
            (len(xArray)) * side,
            scr_height))  # расширяем окно по х, чтобы нарисовать обрезанные клетки
        xArray = np.arange(0, (len(xArray)) * side, side)

    # window = cv2.resize(window, (scr_width, scr_height))  # как фон

    for i in range(len(yArray) - 1):
        isBlackStart = not isBlackStart
        isBlack = isBlackStart  # бегунок для строчки
        for j in range(len(xArray)):
            if isBlack:
                window[yArray[i]:yArray[i + 1], xArray[j]:xArray[j] + side] = black_cell
                isBlack = False
            else:
                window[yArray[i]:yArray[i + 1], xArray[j]:xArray[j] + side] = white_cell
                isBlack = True

    black_cell = cv2.resize(black_cell, (side, scr_height - yArray[len(yArray) - 1]))
    white_cell = cv2.resize(white_cell, (side, scr_height - yArray[len(yArray) - 1]))
    for i in range(len(xArray)):  # заполение нижнего столбца
        isBlackStart = not isBlackStart
        if isBlackStart:
            window[yArray[len(yArray) - 1]:scr_height, xArray[i]:xArray[i] + side] = black_cell
        else:
            window[yArray[len(yArray) - 1]:scr_height, xArray[i]:xArray[i] + side] = white_cell

    swapBuffer = cv2.imread('girl.jpg')
    swapBuffer = cv2.resize(swapBuffer, (scr_width, scr_height))
    # test
    #

    for i in range(1000):
        swapBuffer = window[:, :scr_width]
        #swapBuffer[-200:,-200:] = img1
        out.write(swapBuffer)
        window = shift(window, (len(xArray)) * side)

    out.release()
    lbl6.config(text="done")
    # cv2.imshow('program', window)
    # cv2.waitKey(0)


window = Tk()
window.title("vkr")
window.geometry('300x190')

lbl1 = Label(window, text="Диагональ монитора (дюйм): ", padx=20, pady=5)
lbl1.grid(column=0, row=0)
lbl2 = Label(window, text="Ширина монитора (пикс): ", pady=5)
lbl2.grid(column=0, row=1)
lbl3 = Label(window, text="Высота монитора (пикс): ", pady=5)
lbl3.grid(column=0, row=2)
lbl4 = Label(window, text="Кадров в секунду:", pady=5)
lbl4.grid(column=0, row=3)
lbl5 = Label(window, text="Длительность (сек): ", pady=5)
lbl5.grid(column=0, row=4)

lbl6 = Label(window)
lbl6.grid(column=1, row=5)  # инфополе для вывода инфы что всё готово при завершении

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

startButton = Button(window, text="Начать", command=showVideo, pady=5)
startButton.grid(column=0, row=5)
window.mainloop()
