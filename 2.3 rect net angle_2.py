import random
from python_settings import *
import os
import pandas
import pygame as pg
import matplotlib.pyplot
import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field as ff

name = input("Озаглавьте папку >>> ")

r_screen_width = float(input("Ширина x поля в нанометрах/100 >>> "))
r_screen_height = float(input("Ширина y поля в нанометрах/100 >>> "))
mid_radius = float(input("Радиус в нанометрах/100 >>> "))
screen_width = 1000
screen_height = 500
k = screen_width / r_screen_width

os.mkdir(name)


def structure():
    spheres = []

    def full_random(num_of_spheres):
        spheres.append([0., 0., 0.])

        n = num_of_spheres

        while n > 0:
            i = True
            radius = mid_radius + mid_radius*0.05*(1-2*random.random())
            x_coord, y_coord = (radius + random.random()*(r_screen_width - 2*radius),
                                radius + random.random()*(r_screen_height - 2*radius))
            for sphere in spheres:
                if (sphere[0] - x_coord)**2 + (sphere[1] - y_coord)**2 < (radius + sphere[2]+0.2)**2:
                    i = False
                    break
            if i:
                spheres.append([x_coord, y_coord, radius])
                n -= 1

        spheres.remove([0., 0., 0.])

    def view():
        global screen_width
        global screen_height
        global k

        pg.init()

        screen = pg.display.set_mode((screen_width, screen_height))

        screen.fill((0, 0, 0))

        for sphere in spheres:
            center_x, center_y, radius = sphere[0]*k, sphere[1]*k, sphere[2]*k
            pg.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius)

        pg.image.save(screen, f'{name}/structure.png')
        pg.quit()

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
        while float(n_array[wave_ind][0])*1000 < wave:
            wave_ind += 1
        wave_btw = [wave_ind - 1, wave_ind]
        delta_wave_1 = wave - float(n_array[wave_btw[0]][0])*1000
        delta_wave_2 = float(n_array[wave_btw[1]][0])*1000 - wave
        if delta_wave_2 == 0:
            return float(n_array[wave_btw[1]][1]) + float(n_array[wave_btw[1]][2])*1j
        if delta_wave_1 == 0:
            return float(n_array[wave_btw[0]][1]) + float(n_array[wave_btw[0]][2])*1j
        else:
            scale = delta_wave_1/(delta_wave_2+delta_wave_1)
            delta_1 = abs(float(n_array[wave_btw[1]][1]) - float(n_array[wave_btw[0]][1]))
            delta_2 = abs(float(n_array[wave_btw[1]][2]) - float(n_array[wave_btw[0]][2]))
            return ((abs(float(n_array[wave_btw[0]][1])) + abs(delta_1*scale)) +
                    (abs(float(n_array[wave_btw[0]][2])) + abs(delta_2*scale))*1j)

    def smuthi_calculation_wave(angle):
        global r_screen_width
        global r_screen_height

        spectrum = []

        for wave in range(380, 780, 20):
            spheres_for_smuthi = []

            sphere_ref_ind = get_ref_index(wave, "Si")
            layer_ref_ind = get_ref_index(wave, "SiO2")
            for sphere in spheres:
                print([sphere[0]*100, sphere[1]*100, sphere[2]*100])
                spheres_for_smuthi.append(
                    smuthi.particles.Sphere(
                        position=[sphere[0]*100, sphere[1]*100, sphere[2]*100],
                        refractive_index=sphere_ref_ind,
                        radius=sphere[2]*100,
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

            norm = r_screen_width*r_screen_height*10000

            scs = scs / norm

            spectrum.append([scs, wave])

        return spectrum

    def smuthi_calculation_angle():
        global r_screen_width
        global r_screen_height

        angle_spectrum = []

        angle = 0

        spheres_for_smuthi = []
        wave = 740
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

        while angle < np.pi/2:
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

            norm = r_screen_width*r_screen_height*10000

            scs = scs / norm

            angle_spectrum.append([scs, angle])

            angle += np.pi/40

        return angle_spectrum

    def sum_with_scale(array, delta):
        sum_ = 0
        for i in range(0, len(array) - 1, delta):
            sum_ += (array[i] + array[i + 1]) / 2

        return sum_

    def mult_integral(delta, *args):
        mult_fun = []
        for i in range(0, len(args[0]) - 1, delta):
            el = 1
            for fun in args:
                if args.index(fun) == 1:
                    el *= (fun[int(i * 5 / delta)] + fun[int(i * 5 / delta) + 1]) / 2
                else:
                    el *= (fun[i] + fun[i + 1]) / 2

            mult_fun.append(el)
            print(i)

        return sum_with_scale(mult_fun, delta)

    def cie_from_spectrum(x_graph, y_graph):
        # Считываем функции всоприятия цветов реепторами глаза
        x_ = pandas.read_excel("x2_10deg_05.xlsx")
        y_ = pandas.read_excel("y2_10deg_05.xlsx")
        z_ = pandas.read_excel("z2deg_05.xlsx")

        # Выбираем из тапблицы нужную колонку (1) и строки (1:82)
        x_ = x_.iloc[1:82, 1]
        y_ = y_.iloc[1:82, 1]
        z_ = z_.iloc[1:82, 1]

        delta = abs(x_graph[0] - x_graph[1])

        # Вычисление координат цвета
        pre_coordinates = (mult_integral(delta, x_.tolist(), y_graph),
                           mult_integral(delta, y_.tolist(), y_graph),
                           mult_integral(delta, z_.tolist(), y_graph))

        s = sum(pre_coordinates)

        X = pre_coordinates[0] / s
        Y = pre_coordinates[1] / s

        return [X, Y]




        pg.image.save(screen, f"{name}/cie.png")
        pg.quit()

    full_random(int(input("Кол-во сфер >>> ")))
    view()

    x = []
    y = []
    for f in range (1, 13):
        spec = smuthi_calculation_wave(f/12*np.pi)

        for point in spec:
            x.append(point[1])
            y.append(point[0])

        matplotlib.pyplot.plot(x, y)
        matplotlib.pyplot.xlabel("Wavelength [nm]")
        matplotlib.pyplot.ylabel("Normalized cross-sections")
        matplotlib.pyplot.savefig(f"{name}/spectrum.png")

        matplotlib.pyplot.close()



    max_wave = x[y.index(max(y))]

    x_ang = []
    y_ang = []

    spec_ang = smuthi_calculation_angle()

    for point in spec_ang:
        x_ang.append(point[1])
        y_ang.append(point[0])

    matplotlib.pyplot.plot(x_ang, y_ang)
    matplotlib.pyplot.xlabel("Angle [Rad]")
    matplotlib.pyplot.ylabel("Normalized cross-sections")
    matplotlib.pyplot.savefig(f"{name}/angle_spectrum.png")


structure()