import os
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

    out = cv2.VideoWriter('output.mp4', 0x00000021, int(txt4.get()), (scr_width, scr_height))

    black_cell = cv2.imread('black_cell.jpg')
    white_cell = cv2.imread('white_cell.jpg')

    temp = cv2.imread('black_cell.jpg')
    temp = cv2.resize(temp, (1, scr_height))

    red_banner = cv2.imread('red_cell.jpg')
    red_banner = cv2.resize(red_banner,(scr_width,scr_height))

    diag_pix = sqrt(scr_width ** 2 + scr_height ** 2)  # диагональ в пикселях
    side = int(diag_pix / scr_diag)  # сторона клетки в пикселях (по идее 1 дюйм)

    isBlackStart = False  # переключатель, задающий цвет в начале каждой строки

    xArray = np.arange(0, scr_width, side)
    yArray = np.arange(0, scr_height, side)  # координаты шахматной сетки по x и y
    print(len(xArray),len(yArray))

    black_cell = cv2.resize(black_cell, (side, side))
    white_cell = cv2.resize(white_cell, (side, side))

    window = cv2.imread('girl.jpg')

    if len(xArray) % 2 != 0:  # колво клеток по горизонтали должно быть чётным, чтобы при сдвиге соседние клетки были разного цвета
        print('нечёт')
        window = cv2.resize(window, (
            (len(xArray) + 1) * side,
            scr_height))  # расширяем окно по х, чтобы нарисовать обрезанные клетки
        xArray = np.arange(0, (len(xArray) + 1) * side, side)
    else:
        print('чёт')
        window = cv2.resize(window, (
            (len(xArray)) * side,
            scr_height))  # расширяем окно по х, чтобы нарисовать обрезанные клетки
        xArray = np.arange(0, (len(xArray)) * side, side)

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

    if chvar.get() == 0:  # нумерация qr-кодами
        qrsize = round(scr_width / 5)
        qrnum = 10  # количество вариантов кода
        qrs = []  # варианты
        for i in range(qrnum):
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=0
            )
            qr.add_data(i)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save(f'temp{i}.png')
            img = cv2.imread(f'temp{i}.png')
            img = cv2.resize(img, (qrsize, qrsize))
            qrs.append(img)

        swapBuffert = cv2.imread('girl.jpg')
        swapBuffert = cv2.resize(swapBuffert, (scr_width, scr_height))

        for i in range(duration * fps):
            swapBuffer = window[:, :scr_width]
            swapBuffert[:, :] = swapBuffer[:, :]

            if i % 4 == 0:  # расположение кода в разных углах экрана
                swapBuffert[-qrsize:, -qrsize:] = qrs[i % qrnum]
            if i % 4 == 1:
                swapBuffert[:qrsize, -qrsize:] = qrs[i % qrnum]
            if i % 4 == 2:
                swapBuffert[-qrsize:, :qrsize] = qrs[i % qrnum]
            if i % 4 == 3:
                swapBuffert[:qrsize, :qrsize] = qrs[i % qrnum]

            out.write(swapBuffert)
            window = shift(window, (len(xArray)) * side)

        for i in range(qrnum):  # удаление оставшихся изображений кодов
            os.remove(f'temp{i}.png')

    if chvar.get() == 1:  # нумерация фигурами
        cellsize = round(scr_width / 5)

        redcell = cv2.imread('red_cell.jpg')
        greeencell = cv2.imread('green_cell.jpg')
        bluecell = cv2.imread('blue_cell.jpg')
        yellowcell = cv2.imread('yellow_cell.jpg')
        purplecell = cv2.imread('purple_cell.jpg')

        redcell = cv2.resize(redcell, (cellsize, cellsize))
        greeencell = cv2.resize(greeencell, (cellsize, cellsize))
        bluecell = cv2.resize(bluecell, (cellsize, cellsize))
        yellowcell = cv2.resize(yellowcell, (cellsize, cellsize))
        purplecell = cv2.resize(purplecell, (cellsize, cellsize))

        swapBuffert = cv2.imread('girl.jpg')
        swapBuffert = cv2.resize(swapBuffert, (scr_width, scr_height))

        for i in range(duration * fps):
            swapBuffer = window[:, :scr_width]
            swapBuffert[:, :] = swapBuffer[:, :]
            if i % 5 == 0:  # расположение кода в разных углах экрана
                swapBuffert[-cellsize:, -cellsize:] = redcell
            if i % 5 == 1:
                swapBuffert[:cellsize, -cellsize:] = greeencell
            if i % 5 == 2:
                swapBuffert[-cellsize:, :cellsize] = bluecell
            if i % 5 == 3:
                swapBuffert[:cellsize, :cellsize] = yellowcell
            if i % 5 == 4:
                swapBuffert[:cellsize, :cellsize] = purplecell
            if i < fps*5:
                out.write(red_banner)
            else:
                out.write(swapBuffert)
            window = shift(window, (len(xArray)) * side)

    out.release()
    lbl6.config(text="done")
    # cv2.imshow('program', window)
    # cv2.waitKey(0)


window = Tk()
window.title("vkr")
window.geometry('300x210')

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

startButton = Button(window, text="Начать", command=showVideo, pady=5)
startButton.grid(column=0, row=6)
window.mainloop()
