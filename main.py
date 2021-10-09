from math import sqrt

import cv2
import numpy as np
print("enter monitor diagonal (inches): ")
scr_diag = 21                  #int(input())  # monitor diagonal
print("enter monitor height (pixels): ")
scr_height = 768                       #int(input())
print("enter monitor width (pixels): ")
scr_width = 1024                       #int(input())

black_cell = cv2.imread('black_cell.jpg')
#black_cell = cv2.resize(black_cell,(500,500))

white_cell = cv2.imread('white_cell.jpg')
#white_cell = cv2.resize(white_cell,(250,250))


window = cv2.imread('girl.jpg')
window = cv2.resize(window,(scr_width,scr_height)) # как фон

diag_pix = sqrt(scr_width**2 + scr_height**2) # диагональ в пикселях
side = int(diag_pix/scr_diag)  # сторона клетки в пикселях (по идее 1 дюйм)

isBlackStart = False # тоже переключатель, задающий цвет в начале каждой строки
x = 0
y = 0 # бегунки заполняющие поле
xArray = np.arange(0,scr_width,side)
yArray = np.arange(0,scr_height,side) # координаты шахматной сетки по x и y

#xArray = np.linspace(0,scr_widght,len(xArray)).round() # изменяем массив, чтобы не было обрезанных клеток
#yArray = np.linspace(0,scr_widght,len(yArray)).round() # изменяем массив, чтобы не было обрезанных клеток


black_cell = cv2.resize(black_cell,(side,side))
white_cell = cv2.resize(white_cell,(side,side))

'''
for i in range(len(yArray)-1):
    isBlackStart = not isBlackStart
    isBlack = isBlackStart
    for j in range(len(xArray)-1):
        if isBlack:
            window[yArray[i]:yArray[i+1],xArray[j]:xArray[j+1]] = black_cell
            isBlack = False
        else:
            window[yArray[i]:yArray[i+1], xArray[j]:xArray[j + 1]] = white_cell
            isBlack = True
'''

for i in range(len(yArray)-1):
    isBlackStart = not isBlackStart
    isBlack = isBlackStart
    for j in range(len(xArray)):
        if j == len(xArray)-1: # если последняя клетка, то она будет обрезанной, нужно сначала изменить размер

            if isBlack:
                black_cell = cv2.resize(black_cell,(scr_width-xArray[j],side))
                window[yArray[i]:yArray[i+1],xArray[j]:scr_width] = black_cell
                black_cell = cv2.resize(black_cell, (side, side)) # и обратно
            else:
                white_cell = cv2.resize(white_cell, (scr_width - xArray[j] ,side))
                window[yArray[i]:yArray[i + 1], xArray[j]:scr_width] = white_cell
                white_cell = cv2.resize(white_cell, (side, side))
        else:
            if isBlack:
                window[yArray[i]:yArray[i+1],xArray[j]:xArray[j+1]] =  black_cell
                isBlack = False
            else:
                window[yArray[i]:yArray[i+1], xArray[j]:xArray[j + 1]] = white_cell
                isBlack = True


black_cell = cv2.resize(black_cell,())
for i in range(len(xArray)): # заполение нижнего столбца
    isBlackStart = not isBlackStart
    if





'''
for i in range(len(xArray)-2):
    for j in range(len(yArray)-2):
        if isBlack:
            window[yArray[j]:yArray[j+1],xArray[i]:xArray[i+1]] = black_cell
            isBlack = False
        else:
            window[yArray[j]:yArray[j+1],xArray[i]:xArray[i+1]] = white_cell
            isBlack = True
    isBlack = False
'''
cv2.imshow('program',window)
cv2.waitKey(0)



 #   if x > scr_widght or y > scr_height:
    #    flag = False


#black_cell[250:,250:] = white_cell
#cv2.imshow('program',black_cell)
##cv2.waitKey(0)