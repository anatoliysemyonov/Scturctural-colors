from tkinter import *
# подготовка поля
import numpy as np
from tkinter import *
window = Tk()
c = Canvas(window,width=900, height=900) # Холст 1000
c.pack()
window.title('Структурка') # Заголовок

def circ(x, y, r):
    x1=x-r
    x2=x+r
    y1=y-r
    y2=y+r
    c.create_oval(x1, y1, x2, y2)

import random
def p(a):
    for i in a:
        for j in i:
            print(j, end=" ")
        print()

# задаем размеры подложки
size_x = 2000
size_y = 2000
# размер ячейки, в которую будем помещать сферу
a = 400
b = 400

Na=size_x//a
Nb=size_y//b

arr=[]
for i in range(Na):
    arr.append([])
    for j in range (Nb):
        arr[i].append([])
        for k in range(0, 3):
            arr[i][j].append([])


r=100
for i in range(Na):
    for j in range(Nb):
        arr[i][j][0] = 2*r*i+((-1)**j)*r/2 #сдвиг по иксу в зависимости от четности ряда
        arr[i][j][1] = r*j*np.sqrt(3) #сдвиг по игреку на корень 3
        arr[i][j][2] = r

p(arr)
