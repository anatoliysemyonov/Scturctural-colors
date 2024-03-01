import random
import time
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field as ff
import matplotlib.pyplot as graf
import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field
import smuthi.postprocessing.graphical_output
import smuthi.utility.automatic_parameter_selection
from tkinter import *



countSim = 0
countDraw = 1
countOwl = 1
countPLot = 1
work = 1
materials = []
mathcolors = []
veryNachalo = time.time()

norm = 0



class Material:
    def __init__(self, name):
        self.name = name
        read = open('materials/' + name +'.txt', 'r')  # зачитал файл

        data_n_wl = []  # создал два массива
        data_n = []
        data_n_j = []

        reading = read.readline()
        while reading != " " and reading != "":
            reading = reading.strip()
            reading.replace('.', ',')
            data_n_wl.append(float(reading.split(" ")[0]))
            data_n.append(float(reading.split(" ")[1]))
            data_n_j.append(float(reading.split(" ")[2]))
            reading = read.readline()
        read.close()
        self.n = data_n
        self.wl = data_n_wl
        self.j = data_n_j
        self.length = len(data_n)










def search_wl(left, right, A, B, key):  # бинарный поиск с усреднением относительно соседних
    if right > left + 1:
        middle = int((left + right) / 2)
        if (A[middle] == key):
            return B[middle]
        if A[middle] > key:
            return search_wl(left, middle, A, B, key)
        else:
            return search_wl(middle, right, A, B, key)
    else:
        return (key - A[left]) / (A[right] - A[left]) * (B[right] - B[left]) + B[left]


def thights(size_x, size_y, r, mat):
    Na = size_x // (2*r)
    Nb = size_y // (2*r)
    norm = size_x*size_y

    arr = []  # относительные координаты сфер
    for i in range(Na):
        arr.append([])
        for j in range(Nb):
            arr[i].append([])

            x = r
            y = r
            arr[i][j].append(x)
            arr[i][j].append(y)
            arr[i][j].append(r)
    # p(arr)
    # каждая ячейка массива Na*Nb содержит в себе массив - пару чисел (координаты центра ОТНОСИТЕЛЬНО ЛЕВОГО НИЖНЕГО УГЛА) и радиус

    arr1 = arr  # абсолютные координаты
    for i in range(Na):
        for j in range(Nb):
            arr1[i][j][0] = arr[i][j][0] + 2 * r * i
            arr1[i][j][1] = arr[i][j][1] + 2 * r * j
    spres = open('SpheresList' + str(countOwl) + '.txt', 'a')
    for i in range(Na):
        for j in range(Nb):
            spres.write(str(arr1[i][j][0]) + ";" + str(arr1[i][j][1]) + ";" + str(arr1[i][j][2]) + ";" + str(mat)+ "\n")
    spres.close()
    return norm


def const_r_rect_net(size_x, size_y, a, b, r, mat):
    Na = size_x // a
    Nb = size_y // b
    norm = size_x*size_y

    arr = []  # относительные координаты сфер
    for i in range(Na):
        arr.append([])
        for j in range(Nb):
            arr[i].append([])

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
    spres = open('SpheresList' + str(countOwl) + '.txt', 'a')
    for i in range(Na):
        for j in range(Nb):
            spres.write(str(arr1[i][j][0]) + ";" + str(arr1[i][j][1]) + ";" + str(arr1[i][j][2]) + ";" + str(mat) + "\n")
    spres.close()
    return norm


def full_random(n, a, b, r, dr, mat):
    norm = a*b
    allspheres = []

    spres = open('SpheresList' + str(countOwl) + '.txt', 'r')
    line = spres.readline()
    while (line != ""):
        allspheres.append([int(line.split(";")[0]),int(line.split(";")[1]),int(line.split(";")[2])])
        line = spres.readline()
    spres.close()
    spres = open('SpheresList' + str(countOwl) + '.txt', 'a')

    while n > 0:
        i = True
        radius = random.randint(r-dr, r+dr)
        x, y = random.randint(0 + radius, b - radius), random.randint(0 + radius, a - radius)
        for sphere in allspheres:
            if (sphere[0] - x)**2 + (sphere[1] - y)**2 < (radius + sphere[2])**2:
                i = False
                break
        if i:

            spres.write(str(x) + ";" + str(y) + ";" + str(radius) + ";" +str(mat) + "\n")
            allspheres.append([x, y, radius])
            n -= 1
    spres.close()

    return norm


def triangle_thights(size_x, size_y, a, b, r, mat):
    Na = size_x // a
    Nb = size_y // b
    norm = size_x*size_y
    arr = []
    for i in range(Na):
        arr.append([])
        for j in range(Nb):
            arr[i].append([])
            for k in range(0, 2):
                arr[i][j].append([])

    for i in range(Na):
        for j in range(Nb):
            arr[i][j][0] = a * i + ((-1) ** (j)) * r / 2  # сдвиг по иксу в зависимости от четности ряда
            arr[i][j][1] = r * j * np.sqrt(3)  # сдвиг по игреку на корень 3

    spres = open('SpheresList' + str(countOwl) + '.txt', 'a')
    for i in range(Na):
        for j in range(Nb):
            spres.write(
                str(int(arr[i][j][0])) + ";" + str(int(arr[i][j][1])) + ";" + str(r) + ";" + str(mat) + "\n")
    spres.close()

    return norm


def Spectrum(materials, leftGran, rightGran, shag):


    bI = []  # массив с рассеянием
    for i in range(leftGran, rightGran, shag):  # фором пробегаюсь по всем длинам волн (i - длина волны в нм)
        N = 0
        ns = []
        js = []
        sps = open('SpheresList' + str(countOwl) + '.txt', 'r')
        for mat in materials:
            ns.append(search_wl(0, mat.length, mat.wl, mat.n, i / 1000))
            js.append(search_wl(0, mat.length, mat.wl, mat.j, i / 1000))

        two_layers = smuthi.layers.LayerSystem(thicknesses=[0, 0],  # просто стандартные два полупространства
                                               refractive_indices=[ns[int(podstilka)] + js[int(podstilka)]*1j, 1])




        spheres = []  # наделал сферок(чтоб каждая расчитывалась в зависимости от длины волны)
        line = sps.readline()
        while(line != ""):
            N = N+1
            spheres.append(
                smuthi.particles.Sphere(position=[int(line.split(";")[0]), int(line.split(";")[1]), int(line.split(";")[2])],
                                        refractive_index=ns[int(line.split(";")[3])] + js[int(line.split(";")[3])]*1j,
                                        radius=int(line.split(";")[2]),
                                        l_max=3)
            )
            line = sps.readline()




        plane_wave = smuthi.initial_field.PlaneWave(vacuum_wavelength=i,  # насветил, i - это длина волны
                                                    polar_angle=np.pi,
                                                    azimuthal_angle=0,
                                                    polarization=0)

        simulation = smuthi.simulation.Simulation(layer_system=two_layers,
                                                  particle_list=spheres,
                                                  solver_type='gmres',
                                                  solver_tolerance=1e-7,
                                                  initial_field=plane_wave)

        simulation.run()


        scs = ff.total_scattering_cross_section(initial_field=plane_wave,  # evaluate the scattering cross section
                                                particle_list=spheres,
                                                layer_system=two_layers)
        scs = scs / norm

        print(i)  # просто вывод, чтоб следить за процессом
        print(scs)
        bI.append(scs)
        sps.close()
    return bI






f = open('command.txt', 'r')  # зачитал файл

s = open('SpheresList' + str(countOwl) + '.txt', 'w') #почистил массив(текстовый файл) сфер
s.truncate()
s.close()
s2 = open('output.txt', 'w')  #почистил вывод
s2.truncate()
s2.close()





while work == 1:
    cmd = f.readline()  # прочитал строку
    cmd = cmd.replace("\n", "")
    cmds = cmd.split(";")
    i = 1
    while i == 1:

        if cmds[0] == "":  # конец программы
            work = 0
            break

        if cmds[0] == "SimulateSpectrum":
            begin = time.time()
            y = Spectrum(materials, int(cmds[1]), int(cmds[2]), int(cmds[3]))

            x = []
            for i in range(int(cmds[1]), int(cmds[2]), int(cmds[3])):                       # массив иксов, чтоб график построить
                x.append(i)

            graf.plot(x, y)                                                                    # строю графек

            out = open('output.txt', 'a')
            vrem = time.time() - begin
            out.write("\n" + str(countSim) + ") Proshlo " + str(vrem) + " secund\n")
            countSim = countSim + 1
            out.close()
            if len(cmds) > 4:
                if cmds[4] == "Save":
                    graf.savefig(str(countSim) + "section.png")
                    plot = open(str(countPLot) + 'plot.txt', 'w')
                    countPLot = countPLot + 1
                    for i in range(0, len(x), 1):
                        plot.write(str(x[i]) + " " + str(y[i]) + "\n")
                    plot.close()
                else:
                    graf.show()
            else:
                graf.show()
            graf.close()
            break

        if cmds[0] == "OneSphere":                                                          #добавление сферы
            sprs = open('SpheresList' + str(countOwl) + '.txt', 'a')                        # записал сферки
            sprs.write(cmds[1] + ";" + cmds[2] + ";" + cmds[3] + ";" + cmds[4]+"\n")        #сфера добавляется так: x;y;r;номер материала
            sprs.close()
            break

        if cmds[0] == "AddMaterial":
            materials.append(Material(cmds[1]))
            mathcolors.append([random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)])
            break

        if cmds[0] == "Draw":
            window = Tk()
            c = Canvas(window, width=1920, height=1080)
            c.pack()
            sps = open('SpheresList' + str(countOwl) + '.txt', 'r')
            line = sps.readline()
            while line != "":
                m = int(line.split(";")[3])
                c.create_oval(int(line.split(";")[0])/20-int(line.split(";")[2])/20, int(line.split(";")[1])/20-int(line.split(";")[2])/20, int(line.split(";")[0])/20+int(line.split(";")[2])/20, int(line.split(";")[1])/20+int(line.split(";")[2])/20, fill='#{:02x}{:02x}{:02x}'.format( int(mathcolors[m][0]), int(mathcolors[m][1]), int(mathcolors[m][2]) ))
                line = sps.readline()
            sps.close()
            window.mainloop()
            break

        if cmds[0] == "RectNet":
            norm = const_r_rect_net(int(cmds[1]),int(cmds[2]),int(cmds[3]),int(cmds[4]),int(cmds[5]), int(cmds[6]))
            break

        if cmds[0] == "Random":
            norm = full_random(int(cmds[1]),int(cmds[2]),int(cmds[3]),int(cmds[4]),int(cmds[5]), int(cmds[6]))
            break

        if cmds[0] == "ThightsRectNet":
            norm = thights(int(cmds[1]),int(cmds[2]),int(cmds[3]),int(cmds[4]))
            break

        if cmds[0] == "ThightsTriNet":
            norm = triangle_thights(int(cmds[1]),int(cmds[2]),int(cmds[3]),int(cmds[4]),int(cmds[5]),int(cmds[6]))
            break

        if cmds[0] == "Clear":
            ssss = open('SpheresList' + str(countOwl) + '.txt', 'w')
            ssss.truncate()
            ssss.close()
            break

        if cmds[0] == "Podstilka":
            podstilka = cmds[1]
            break

        if cmds[0] == "Owl":
            countOwl = countOwl + 1
            break

        print("Something is creating script ERRORs")
        i = 0  # почему нет switch case пришлось костылить...

out = open('output.txt', 'a')                                   #отчёт о времени
out.write("\n Vsego proshlo " +str(time.time() - veryNachalo))
out.close()
