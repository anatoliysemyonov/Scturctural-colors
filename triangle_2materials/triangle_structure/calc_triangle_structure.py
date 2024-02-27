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




                                #начальные условия
leftGran = 380                  #минимальная длина волны, нм
rightGran = 790                 #максимальная длина волны, нм
shag = 10                     #шаг, с коротым будут ставиться точки(длина волны, нм)




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






f = open('/Users/annabizukova/PycharmProjects/pythonProject_test/smuthi/silicon.txt', 'r')           #зачитал файл
reading = f.read()

data_n_wl = [] #создал три массива
data_n = []
data_ni = []

z = 1

for symbol1 in reading.split("\n"):
 for symbol in symbol1.split("\t"):
     if (z % 3 == 0):
         data_n_wl.append(float(symbol))  #добавляю поочередно длину волны и n
     elif(z % 3 == 1):
         data_n.append(float(symbol))
     else:
         data_ni.append(float(symbol))
     z = z + 1


# задаем размеры подложки
size_x = 1800
size_y = 1800
# размер ячейки, в которую будем помещать сферу
a = 200
b = 200
r = 100

Na = size_x//a
Nb = size_y//b

arr = []
for i in range(Na):
    arr.append([])
    for j in range (Nb):
        arr[i].append([])
        for k in range(0, 2):
            arr[i][j].append([])



for i in range(Na):
    for j in range(Nb):
        arr[i][j][0] = a*i + ((-1) ** (j)) * r/2  #сдвиг по иксу в зависимости от четности ряда
        arr[i][j][1] = r*j*np.sqrt(3) #сдвиг по игреку на корень 3


bI = [] #массив с рассеянием
for i in range(leftGran, rightGran, shag): #фором пробегаюсь по всем длинам волн (i - длина волны в нм)

    n_1 = search_wl(0, len(data_n), data_n_wl, data_n, i / 1000)  # заранее считаю коэффициент преломления для материала 1
    ni_1 = search_wl(0, len(data_ni), data_n_wl, data_ni,
                   i / 1000)  # заранее считаю коэффициент преломления для материала 1
    n_2 = search_wl(0, len(data_n), data_n_wl, data_n, i/1000) #заранее считаю коэффициент преломления для материала 2
    ni_2 = search_wl(0, len(data_ni), data_n_wl, data_ni, i/1000) #заранее считаю коэффициент преломления для материала 2

    two_layers = smuthi.layers.LayerSystem(thicknesses=[0, 0],          # просто стандартные два полупространства
                                           refractive_indices=[n_1+ni_1*1j, 1])




    spheres = []                                        #наделал сферок(чтоб каждая расчитывалась в зависимости от длины волны)



    for k in range(len(arr)):
        for j in range(len(arr[k])):
            spheres.append(
                smuthi.particles.Sphere(position=[arr[k][j][0], arr[k][j][1], r],
                                refractive_index = n_2+ni_2*1j,
                                radius = r,
                                l_max = 3)
                          )




    plane_wave =smuthi.initial_field.PlaneWave(vacuum_wavelength=i,     #насветил, i - это длина волны
                                                polar_angle=np.pi,
                                                azimuthal_angle=0,
                                                polarization=0)


    simulation = smuthi.simulation.Simulation(layer_system=two_layers,
                                              particle_list=spheres,
                                              solver_type='gmres',
                                              solver_tolerance=1e-5,
                                              initial_field=plane_wave)

    simulation.run()

    scs = ff.total_scattering_cross_section(initial_field=plane_wave,   # evaluate the scattering cross section
                                                particle_list=spheres,
                                                layer_system=two_layers)
    scs = scs/(size_x * size_y)

    bI.append(scs)


x = []
for i in range(leftGran, rightGran, shag): #массив иксов, чтоб график построить
    x.append(i)

f = open("/Users/annabizukova/PycharmProjects/pythonProject_test/smuthi/triangle_silicon_81spheres.txt", "w")
for i in range(len(x)):
    f.write(str(x[i])+ " "+str( bI[i]) + str('\n'))
f.close()

G.plot(x, bI)  #строю графек
G.show()

