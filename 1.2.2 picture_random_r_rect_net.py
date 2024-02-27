from tkinter import *
window = Tk()
c = Canvas(window,width=1000, height=1000) # Холст 1000
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
size_x=1000
size_y=1000
# размер ячейки, в которую будем помещать сферу
a = 25
b = 25

Na=size_x//a
Nb=size_y//b

arr=[] # относительные координаты сфер
for i in range(Na):
    arr.append([])
    for j in range (Nb):
        arr[i].append([])

        r_max=10
        r_min=8

        x=random.randint(r_max+1, a-r_max-1)
        y=random.randint(r_max+1, b-r_max-1)
        r=random.randint(r_min, r_max)
        arr[i][j].append(x)
        arr[i][j].append(y)
        arr[i][j].append(r)
arr1=arr # абсолютные координаты
for i in range(Na):
    for j in range(Nb):
        arr1[i][j][0]=arr[i][j][0]+a*i
        arr1[i][j][1] = arr[i][j][1]+b*j

p(arr1)


for i in arr1:
    for j in i:
        circ(j[0], j[1], j[2])


window.mainloop()
