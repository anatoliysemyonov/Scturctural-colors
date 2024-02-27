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


def get_ref_index(wave, material):
    dependencies = {
        "SiO2": "SiO2_Gao.txt",
        "Si": "Si_Vuye_20C.txt"
    }
    file = open(dependencies[material], "r")
    lines = file.readlines()
    n_array = []
    for line in lines:
        while line[0] == " ":
            line = line[1:]
        n_array.append(line.split(" "))

    wave_ind = 0
    while float(n_array[wave_ind][0]) * 1000 < wave:
        wave_ind += 1
    wave_btw = [wave_ind - 1, wave_ind]
    delta_wave_1 = wave - float(n_array[wave_btw[0]][0]) * 1000
    delta_wave_2 = float(n_array[wave_btw[1]][0]) * 1000 - wave
    if delta_wave_2 == 0:
        return float(n_array[wave_btw[1]][1]) + float(n_array[wave_btw[1]][2]) * 1j
    if delta_wave_1 == 0:
        return float(n_array[wave_btw[0]][1]) + float(n_array[wave_btw[0]][2]) * 1j
    else:
        scale = delta_wave_1 / (delta_wave_2 + delta_wave_1)
        delta_1 = abs(float(n_array[wave_btw[1]][1]) - float(n_array[wave_btw[0]][1]))
        delta_2 = abs(float(n_array[wave_btw[1]][2]) - float(n_array[wave_btw[0]][2]))
        return ((abs(float(n_array[wave_btw[0]][1])) + abs(delta_1 * scale)) +
                (abs(float(n_array[wave_btw[0]][2])) + abs(delta_2 * scale)) * 1j)


def smuthi_calculation_with_some_angles(spheres):
    spectrum_with_some_angles = []

    for angle in [np.pi, np.pi * 5 / 6, np.pi * 2 / 3]:
        waves = []
        scss = []

        for wave in range(380, 800, 20):
            spheres_for_smuthi = []

            sphere_ref_ind = get_ref_index(wave, "Si")
            layer_ref_ind = get_ref_index(wave, "SiO2")
            for sphere in spheres:
                print([sphere[0] * 100, sphere[1] * 100, sphere[2] * 100])
                spheres_for_smuthi.append(
                    smuthi.particles.Sphere(
                        position=[sphere[0] * 100, sphere[1] * 100, sphere[2] * 100],
                        refractive_index=sphere_ref_ind,
                        radius=sphere[2] * 100,
                        l_max=3
                    )
                )

            layers = smuthi.layers.LayerSystem(thicknesses=[0, 0], refractive_indices=[layer_ref_ind, 1])

            plane_wave = smuthi.initial_field.PlaneWave(
                vacuum_wavelength=wave,
                polar_angle=angle,
                azimuthal_angle=0,
                polarization=0
            )

            simulation = smuthi.simulation.Simulation(
                layer_system=layers,
                particle_list=spheres_for_smuthi,
                solver_type='gmres',
                solver_tolerance=1e-7,
                initial_field=plane_wave
            )

            simulation.run()

            scs = ff.total_scattering_cross_section(
                initial_field=plane_wave,
                particle_list=spheres_for_smuthi,
                layer_system=layers
            )
            r_screen_width=800
            r_screen_height=800
            norm = r_screen_width * r_screen_height * 10000

            scs = scs / norm

            waves.append(wave)
            scss.append(scs)

        matplotlib.pyplot.plot(waves, scss, label=f"Si, r=100nm, N=4 angle={int(180 * angle / np.pi)}")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.xlabel("Wavelength [nm]")
    matplotlib.pyplot.ylabel("Normalized cross-sections")
    matplotlib.pyplot.show()
    matplotlib.pyplot.savefig(f"spectrum_with_different_angles.png")

    matplotlib.pyplot.close()

        #начальные условия
leftGran = 325                  #минимальная длина волны, нм
rightGran = 900                 #максимальная длина волны, нм
shag = 25                   #шаг, с коротым будут ставиться точки(длина волны, нм)
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
size_x = 800
size_y = 800
# размер ячейки, в которую будем помещать сферу
a = 400
b = 400

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
leftGran = 380                  #минимальная длина волны, нм
rightGran = 780

diapasons=[ [380, 780, 10]]
arr_waves = []
for i in diapasons:
    for j in range(i[0], i[1], i[2]):
        arr_waves.append(j)


                #максимальная длина волны, нм
shag = 25                   #шаг, с коротым будут ставиться точки(длина волны, нм)
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
size_x = 1500
size_y = 1500
# размер ячейки, в которую будем помещать сферу
a = 250
b = 250

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

f = open("results/1.1 constant r rect net/file1.txt", "a")
f.write(str(size_x)+" "+str( size_y)+" "+str(a)+" "+str(b)+" "+str((size_y//b)*(size_x//a))+str(r)+"\n")
for i in range(len(x)):
    f.write(str(x[i])+" " + str(bI[i])+"\n")
f.close()

G.plot(x, bI) #строю графек
G.show()
G.close()
#smuthi_calculation_with_some_angles(arr)
print(arr)