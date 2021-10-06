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


girl_img = cv2.imread('girl.jpg')
girl_img = cv2.resize(girl_img,(scr_widght,scr_height)) # как фон

diag_pix = sqrt(scr_widght**2 + scr_height**2) # диагональ в пикселях
side = int(diag_pix/scr_diag)  # сторона клетки в пикселях (по идее 1 дюйм)

isBlack = False # переключатель цвета клетки
x = 0
y = 0 # бегунки заполняющие поле
xArray = np.arange(0,scr_widght,side)
yArray = np.arange(0,scr_height,side)




 #   if x > scr_widght or y > scr_height:
    #    flag = False


#black_cell[250:,250:] = white_cell
#cv2.imshow('program',black_cell)
##cv2.waitKey(0)