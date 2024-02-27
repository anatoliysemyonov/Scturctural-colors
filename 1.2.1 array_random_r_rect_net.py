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
a = 40
b = 40

Na=size_x//a
Nb=size_y//b

arr=[] # относительные координаты сфер
for i in range(Na):
    arr.append([])
    for j in range (Nb):
        arr[i].append([])

        r_max=10
        r_min=7

        x=random.randint(r_max+1, a-r_max-1)
        y=random.randint(r_max+1, b-r_max-1)
        r=random.randint(r_min, r_max)
        arr[i][j].append(x)
        arr[i][j].append(y)
        arr[i][j].append(r)
p(arr)
# каждая ячейка массива Na*Nb содержит в себе массив - пару чисел (координаты центра ОТНОСИТЕЛЬНО ЛЕВОГО НИЖНЕГО УГЛА) и радиус
print()
arr1=arr # абсолютные координаты
for i in range(Na):
    for j in range(Nb):
        arr1[i][j][0]=arr[i][j][0]+i*a
        arr1[i][j][1] = arr[i][j][1]+b*j

p(arr1)