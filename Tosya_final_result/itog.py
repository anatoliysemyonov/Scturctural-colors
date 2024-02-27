import random
import matplotlib.pyplot
import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field as ff

spheres = []

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

        dr = 5
        r = 100
        r0 = r + dr
        q = 0.5    # степень беспорядка. от 0 до 1
        x0 = a / 2
        dx_max = a / 2 - r
        dx = dx_max * q
        y0 = b / 2
        dy_max = b / 2 - r
        dy = dy_max * q

        x = random.randint(int(x0 - dx), int(x0 + dx))
        y = random.randint(int(y0 - dy), int(y0 + dy))
        r = r + dr * random.randint(-1, 1)

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
        arr1[i][j][2] = arr[i][j][2]

for i in arr1:
    for j in i:
        spheres.append(j)

def angle():
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

    def smuthi_calculation_with_some_angles():
        spectrum_with_some_angles = []

        for angle in [np.pi, np.pi-np.pi/4, np.pi*2/3]:
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

                norm = pow(10, 8)

                scs = scs / norm

                waves.append(wave)
                scss.append(scs)

            matplotlib.pyplot.plot(waves, scss, label=f"Si, r=100nm, N=36 angle={int(180*angle/np.pi)}")

        matplotlib.pyplot.legend()
        matplotlib.pyplot.xlabel("Wavelength [nm]")
        matplotlib.pyplot.ylabel("Normalized cross-sections")
        matplotlib.pyplot.savefig(f"spectrum_with_different_angles.png")

        matplotlib.pyplot.close()

    smuthi_calculation_with_some_angles()

angle()