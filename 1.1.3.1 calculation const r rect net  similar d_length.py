import numpy as np
import bisect
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field as ff
import matplotlib.pyplot as G
import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field
import smuthi.postprocessing.graphical_output
import smuthi.utility.automatic_parameter_selection
import random




                                #начальные условия
leftGran = 380                 #минимальная длина волны, нм
rightGran = 780                 #максимальная длина волны, нм
shag = 5                   #шаг, с коротым будут ставиться точки(длина волны, нм)
material_1 = "ZBLAN fluoride glass"       #добавляем материал(имя материала в файле material.txt)



def search_wl(left, right, A, B, key): #бинарный поиск с усреднением относительно соседних
    if right > left + 1:
        middle = int((left + right) / 2)
        if(A[middle] == key):
            return B[middle]
        if A[middle] > key:
            return search_wl(left, middle, A, B, key)
        else:
            return search_wl(middle, right, A, B, key)
    else:
        return (key - A[left])/ (A[right]-A[left]) * (B[right]-B[left])+B[left]






f = open('material.txt', 'r')           #зачитал файл
reading = f.read()

reading = reading.split(material_1)[1]
reading_wl = reading.split("\n")[1]
reading_n = reading.split("\n")[2]      #попилил строки(костыль), получил в строке два нужных массива

data_n_wl = [] #создал два массива
data_n = []

for symbol in reading_wl.split(","):                # два массива data_n_wl с длинами волн и data_n с значениями коэффициента преломления
    data_n_wl.append(float(symbol))                 #в этом куске кода я заполняю эти массивы, читая reading
for symbol in reading_n.split(","):
    data_n.append(float(symbol))


def p(a):
    for i in a:
        for j in i:
            print(j, end=" ")
        print()


# задаем размеры подложки
size_x =1200
size_y = 1200
# размер ячейки, в которую будем помещать сферу
a = 400
b = 400

Na = size_x // a
Nb = size_y // b

arr = []  # относительные координаты сфер
for i in range(Na):
    arr.append([])
    for j in range(Nb):
        arr[i].append([])

        r = 100

        x = random.randint(r + 1, a - r - 1)
        y = random.randint(r + 1, b - r - 1)
        arr[i][j].append(x)
        arr[i][j].append(y)
        arr[i][j].append(r)
# p(arr)
# каждая ячейка массива Na*Nb содержит в себе массив - пару чисел (координаты центра ОТНОСИТЕЛЬНО ЛЕВОГО НИЖНЕГО УГЛА) и радиус

arr1 = arr  # абсолютные координаты
for i in range(Na):
    for j in range(Nb):
        arr1[i][j][0] = arr[i][j][0] + a * i
        arr1[i][j][1] = arr[i][j][1] + b * j

p(arr1)

bI = [] #массив с рассеянием
for i in range(leftGran, rightGran, shag): #фором пробегаюсь по всем длинам волн (i - длина волны в нм)


    n = search_wl(0, len(data_n), data_n_wl, data_n, i/1000) #заранее считаю коэффициент преломления для материала 1




    two_layers = smuthi.layers.LayerSystem(thicknesses=[0, 0],          # просто стандартные два полупространства
                                           refractive_indices=[n, 1])




    spheres = []                                        #наделал сферок(чтоб каждая расчитывалась в зависимости от длины волны)




    for i in range(len(arr1)):
        for j in range(len(arr1[i])):
            spheres.append(
                smuthi.particles.Sphere(position=[arr1[i][j][0], arr1[i][j][1], 100],
                                refractive_index=n,
                                radius=arr[i][j][2],
                                l_max=3)
    )




    plane_wave =smuthi.initial_field.PlaneWave(vacuum_wavelength=i,     #насветил, i - это длина волны
                                                polar_angle=np.pi,
                                                azimuthal_angle=0,
                                                polarization=0)




   # simulation = smuthi.simulation.Simulation(layer_system=two_layers,   #старый добрый кот
   #                                          particle_list=spheres,
   #                                          initial_field=plane_wave)
    # типа быстрый метод
    simulation = smuthi.simulation.Simulation(layer_system=two_layers,
                                              particle_list=spheres,
                                              solver_type='gmres',
                                              solver_tolerance=1e-5,
                                              initial_field=plane_wave)






    #neff_max=test_balloon_simulation.neff_max,
    #neff_resolution=test_balloon_simulation.neff_resolution
    simulation.run()

   # show far field



    scs = ff.total_scattering_cross_section(initial_field=plane_wave,   # evaluate the scattering cross section
                                            particle_list=spheres,
                                            layer_system=two_layers)
    scs = scs/1e6


    print(i)    #просто вывод, чтоб следить за процессом
    print(scs)
    bI.append(scs)


x = []
for i in range(leftGran, rightGran, shag): #массив иксов, чтоб график построить
    x.append(i)

f = open("results/1.1 constant r rect net/file1.txt", "w")
f.write(str(size_x)+" "+str( size_y)+" "+str(a)+" "+str(b)+" "+str((size_y//b)*(size_x//a))+str(r)+"\n")
for i in range(len(x)):
    f.write(str(x[i])+ " "+str( bI[i]))
f.close()

G.plot(x, bI) #строю графек
G.show()

