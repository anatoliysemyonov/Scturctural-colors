
import random
def p(a):
    for i in a:
        for j in i:
            print(j, end=" ")
        print()

# задаем размеры подложки
size_x=2000
size_y=2000
# размер ячейки, в которую будем помещать сферу
a = 400
b = 400

Na=size_x//a
Nb=size_y//b

arr=[] # относительные координаты сфер
for i in range(Na):
    arr.append([])
    for j in range (Nb):
        arr[i].append([])

        r=100

        x=random.randint(r+1, a-r-1)
        y=random.randint(r+1, b-r-1)
        arr[i][j].append(x)
        arr[i][j].append(y)
        arr[i][j].append(r)
#p(arr)
# каждая ячейка массива Na*Nb содержит в себе массив - пару чисел (координаты центра ОТНОСИТЕЛЬНО ЛЕВОГО НИЖНЕГО УГЛА) и радиус

arr1=arr # абсолютные координаты
for i in range(Na):
    for j in range(Nb):
        arr1[i][j][0]=arr[i][j][0]+a*i
        arr1[i][j][1] = arr[i][j][1]+b*j

p(arr1)


