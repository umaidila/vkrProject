from math import sqrt

import cv2
import numpy as np
print("enter monitor diagonal (inches): ")
scr_diag = int(input())  # monitor diagonal
print("enter monitor height (pixels): ")
scr_height = int(input())
print("enter monitor height (pixels): ")
scr_widght = int(input())

black_cell = cv2.imread('black_cell.jpg')
#black_cell = cv2.resize(black_cell,(500,500))

white_cell = cv2.imread('white_cell.jpg')
#white_cell = cv2.resize(white_cell,(250,250))


window = cv2.imread('girl.jpg')
window = cv2.resize(window,(scr_widght,scr_height)) # как фон

diag_pix = sqrt(scr_widght**2 + scr_height**2) # диагональ в пикселях
side = int(diag_pix/scr_diag)  # сторона клетки в пикселях (по идее 1 дюйм)

isBlack = False # переключатель цвета клетки
x = 0
y = 0 # бегунки заполняющие поле
xArray = np.arange(0,scr_widght,side)
yArray = np.arange(0,scr_height,side) # координаты шахматной сетки по x и y

xArray = np.linspace(0,scr_widght,len(xArray)) # изменяем массив, чтобы не было обрезанных клеток
yArray =




black_cell = cv2.resize(black_cell,(side,side))
white_cell = cv2.resize(white_cell,(side,side))




flagX = True
flagY = True
for i in range(len(xArray)-1):
    for j in range(len(yArray)-1):
        if isBlack:
            window[xArray[i]:xArray[i+1],yArray[j]:yArray[j+1]] = black_cell
            isBlack = False
        else:
            window[xArray[i]:xArray[i + 1], yArray[j]:yArray[j + 1]] = white_cell
            isBlack = True
 #   window[xArray]
    isBlack = False

cv2.imshow('program',window)



 #   if x > scr_widght or y > scr_height:
    #    flag = False


#black_cell[250:,250:] = white_cell
#cv2.imshow('program',black_cell)
##cv2.waitKey(0)