import random
from settings import *
import os
import colour
import pandas
import pygame as pg
import matplotlib.pyplot
import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field as ff

instructions = open("instructions.txt", "r")

instructions_lines = instructions.readlines()

cie_coords = []


def structure(instruction):
    instruction_array = instruction.split(";")

    name = instruction_array[0]

    r_screen_width = float(instruction_array[1])
    r_screen_height = float(instruction_array[2])
    mid_radius = float(instruction_array[3])
    number_of_spheres = int(instruction_array[4])
    screen_width = 1000
    screen_height = 500
    k = screen_width / r_screen_width

    os.mkdir(name)

    spheres = []

    def rectangle():
        Na = int(r_screen_width // (2 * mid_radius))
        Nb = int(r_screen_height // (2 * mid_radius))
        norm = r_screen_width*r_screen_height*10000

        arr = []  # относительные координаты сфер
        for i in range(Na):
            for j in range(Nb):
                x = mid_radius * i
                y = mid_radius * j
                arr.append([x, y, mid_radius])

        return arr

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
        pg.init()

        screen = pg.display.set_mode((screen_width, screen_height))

        screen.fill((255, 255, 255))

        for sphere in spheres:
            center_x, center_y, radius = sphere[0]*k, sphere[1]*k, sphere[2]*k
            pg.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)

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

    def smuthi_calculation_wave():
        spectrum = []

        for wave in range(380, 800, 20):
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
                polar_angle=np.pi,
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

    def smuthi_calculation_with_some_angles():
        spectrum_with_some_angles = []

        for angle in [np.pi, np.pi*5/6, np.pi*2/3]:
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

                norm = r_screen_width*r_screen_height*10000

                scs = scs / norm

                waves.append(wave)
                scss.append(scs)

            matplotlib.pyplot.plot(waves, scss, label=f"{name} angle={int(180*angle/np.pi)}")

        matplotlib.pyplot.legend()
        matplotlib.pyplot.xlabel("Wavelength [nm]")
        matplotlib.pyplot.ylabel("Normalized cross-sections")
        matplotlib.pyplot.savefig(f"{name}/spectrum_with_different_angles.png")

        matplotlib.pyplot.close()

    def sum_with_scale(array, delta):
        sum_ = 0
        for i in range(0, len(array) - 1, delta//5):
            sum_ += (array[i] + array[i + 1]) / 2

        return sum_*delta

    def mult_integral(delta, *args):
        mult_fun = []
        for i in range(0, len(args[0]) - 1, delta//5):
            el = 1
            for fun in args:
                if args.index(fun) == 1:
                    print(int(i * 5 / delta), len(args[1]), len(args[0]))
                    el *= (fun[int(i * 5 / delta)] + fun[int(i * 5 / delta) + 1]) / 2
                else:
                    el *= (fun[i] + fun[i + 1]) / 2

            mult_fun.append(el)
            # print(i)

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
        Z = pre_coordinates[2] / s

        return colour.XYZ_to_xy([X, Y, Z])

    def cie_graph(coordinates, n):
        pg.init()

        cie_coords.append([coordinates, n])

        screen = pg.display.set_mode((800, 816))

        bg = pg.image.load("cie_img.png")

        screen.blit(bg, (0, 0))

        x_cie = coordinates[0]
        y_cie = coordinates[1]
        rgb = (0, 0, 0)
        pg.draw.circle(
            screen,
            rgb,
            (OFFSET_X + x_cie * GLOBAL_DELTA_X / LOCAL_DELTA_X,
             816 - (OFFSET_Y + y_cie * GLOBAL_DELTA_Y / LOCAL_DELTA_Y)),
            3
        )

        font = pg.font.SysFont("chalkduster.ttf", 48)
        text = font.render(f'{n}', True, (0, 0, 0))
        screen.blit(text, (400, 40))

        pg.image.save(screen, f"{name}/cie_{n}.png")
        pg.quit()

    full_random(number_of_spheres)
    # spheres = rectangle()
    view()

    x = []
    y = []

    spec = smuthi_calculation_wave()

    spectrum_string = ""

    for point in spec:
        x.append(point[1])
        y.append(point[0])
        spectrum_string = f"{spectrum_string  }{point[1]} {point[0]}\n"

    spectrum_file = open(f"{name}/spectrum.txt", "w")

    spectrum_file.write(spectrum_string)
    spectrum_file.close()

    matplotlib.pyplot.plot(x, y, label=f"{name}")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.xlabel("Wavelength [nm]")
    matplotlib.pyplot.ylabel("Normalized cross-sections")
    matplotlib.pyplot.savefig(f"{name}/spectrum.png")

    matplotlib.pyplot.close()

    cie_graph(cie_from_spectrum(x, y), name)

    smuthi_calculation_with_some_angles()


for inst in instructions_lines:
    structure(inst)


string = ""
for coord in cie_coords:
    string = f"{string}{coord[0]}  {coord[1]}"

file = open("cie_coordinates.txt", "w")
file.write(string)
file.close()
