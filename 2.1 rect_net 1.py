import random
def p(a):
    for i in a:
        for j in i:
            print(j, end=" ")
        print()

# задаем размеры подложки
size_x=2400
size_y=2400
# размер ячейки, в которую будем помещать сферу
a = 600
b = 600
# радиус
r = 250
e_dr = 0.05 # погрешность радиуса 5%
dr=r*e_dr
Na=size_x//a
Nb=size_y//b
N=Na*Nb
arr=[] # относительные координаты сфер
for i in range(Na):
    arr.append([])
    for j in range (Nb):
        arr[i].append([])

        r=random.uniform(r-dr, r+dr)
        x=random.uniform(r+dr+1, a-r-dr-1)
        y=random.uniform(r+dr+1, b-r-dr-1)
        z=r

        arr[i][j].append(round(x+i*a, 2))
        arr[i][j].append(round(y+j*b, 2))
        arr[i][j].append(round(z, 2))
        arr[i][j].append(round(r, 2))
#p(arr)
# каждая ячейка массива Na*Nb содержит в себе массив - пару чисел (координаты центра ОТНОСИТЕЛЬНО ЛЕВОГО НИЖНЕГО УГЛА) и радиус

arr1=arr # абсолютные координаты
for i in range(Na):
    for j in range(Nb):
        arr1[i][j][0] = round(arr[i][j][0]+a*i, 2)
        arr1[i][j][1] = round(arr[i][j][1]+b*j, 2)
print(N)
p(arr1)


