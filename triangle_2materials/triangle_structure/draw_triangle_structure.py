from tkinter import *
# подготовка поля
import numpy as np
from tkinter import *
window = Tk()
c = Canvas(window,width=1200, height=1200) # Холст 1000
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
size_x = 900
size_y = 900
# размер ячейки, в которую будем помещать сферу
a = 200
b = 200
r = 100

Na = size_x//a
Nb = size_y//b

arr = []
for i in range(Na):
    arr.append([])
    for j in range(Nb):
        arr[i].append([])
        for k in range(0, 2):
            arr[i][j].append([])



for i in range(Na):
    for j in range(Nb):
        arr[i][j][0] = a*i+((-1)**(j))*r/2 #сдвиг по иксу в зависимости от четности ряда
        arr[i][j][1] = r*j*np.sqrt(3) + r + 3 #сдвиг по игреку на корень 3
        #arr[i][j][0] = a * i + 1 * r
        #arr[i][j][1] = b * j + 1 * r  #прямоугольная решетка...

p(arr)


for i in arr:
    for j in i:
        circ(j[0], j[1], r)


window.mainloop()

