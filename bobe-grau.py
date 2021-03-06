#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Ejemplo parseo argumentos

#Grupo: Bobe Julio y Grau Marianela.

import argparse
import matplotlib.pyplot as plt
import numpy as np
import random
import math

CONSTANTE_REPULSION = 0.1
CONSTANTE_REPULSION_POBLADO = 0.3
CONSTANTE_ATRACCION = 0.9
CONSTANTE_ATRACCION_POBLADO = 0.15

RELACION_ARISTAS_VERTICES = 1.6

ESPACIO_LIBRE = 0.1

CONSTANTE_TEMPERATURA = 0.95
CONSTANTE_ESPARCIMIENTO = 0.1
EPSILON = 0.05

LARGO = 150
ALTO = 150

class LayoutGraph:

    def __init__(self, grafo, iters, refresh, verbose=False):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        verbose: si está encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo

        self.iters = iters
        self.verbose = verbose
        self.refresh = refresh

        # Inicializo estado
        self.posiciones = self.coordenadas_aleatorias(self.grafo[0])

        # Guardo opciones
        if(len(self.grafo[0])/len(self.grafo[1]) < RELACION_ARISTAS_VERTICES):
            self.c1 = CONSTANTE_REPULSION
            self.c2 = CONSTANTE_ATRACCION
        else:
            self.c1 = CONSTANTE_REPULSION_POBLADO
            self.c2 = CONSTANTE_ATRACCION_POBLADO
        self.temperatura = self.initialize_temperature

        auxiliar = math.sqrt((LARGO * ALTO)/len(self.grafo[0]))
        self.k1 = self.c1 * auxiliar
        self.k2 = self.c2 * auxiliar
        self.centro_pantalla = np.array([0, 0])

    def coordenadas_aleatorias(self, vertices):
        if(self.verbose):
            print("Se están sacando las coordenadas de los vértices del grafo en forma aleatoria.")
        
        posiciones = {}
        mitad_largo = LARGO / 2
        aux1 = mitad_largo* ESPACIO_LIBRE
        mitad_alto = ALTO / 2
        aux2 = mitad_alto* ESPACIO_LIBRE
        rango_x = int(-mitad_largo + aux1) , int(mitad_largo - aux1)
        rango_y = int(-mitad_alto + aux2) , int(mitad_alto - aux2)
        for v in vertices:
            posiciones[v] = np.array([random.randrange(rango_x[0], rango_x[1]), random.randrange(rango_y[0], rango_y[1])])
        return posiciones


    def setear_ejes(self):
        ax = plt.gca()
        mitad = LARGO / 2
        ax.set_xlim([-mitad, mitad])
        mitad = ALTO / 2
        ax.set_ylim([-mitad, mitad])

    @property
    def initialize_temperature(self):
        return LARGO / 10

    def update_temperature(self):
        self.temperatura *= CONSTANTE_TEMPERATURA

    @property
    def initialize_accumulators(self):
        accum = {}
        for v in self.grafo[0]:
            accum[v] = np.array([0, 0])
        return accum

    def f_attraction(self, distance):
        return distance** 2 / self.k2

    def f_repulsion(self, distance):
        return self.k1** 2 / distance

    def compute_repulsion_forces(self, accum):
        if(self.verbose):
            print("Se está sacando la fuerza de repulsión para afectar a los vértices del grafo.")

        for n_i in self.grafo[0]:
            for n_j in self.grafo[0]:
                if n_i != n_j:
                    distance = np.linalg.norm(self.posiciones[n_i] - self.posiciones[n_j])
                    mod_fa = self.f_repulsion(distance)
                    f = mod_fa * (self.posiciones[n_j] - self.posiciones[n_i]) / distance

                    accum[n_i] = accum[n_i] - f
                    accum[n_j] = accum[n_j] + f

    def compute_attraction_forces(self, accum):
        if(self.verbose):
            print("Se está sacando la fuerza de atracción para afectar a los vértices del grafo.")

        for n_i, n_j in self.grafo[1]:
            distance = np.linalg.norm(self.posiciones[n_i] - self.posiciones[n_j])
            mod_fa = self.f_attraction(distance)
            f = mod_fa * (self.posiciones[n_j] - self.posiciones[n_i]) / distance

            accum[n_i] = accum[n_i] + f
            accum[n_j] = accum[n_j] - f

    def update_positions(self, accum):
        if(self.verbose):
            print("Se actualizan las coordenadas de los vértices del grafo luego de haber sido afectados por la fuerza de atracción, repulsión y la gravedad.")

        for node in self.grafo[0]:
            f = accum[node]
            modulo_f = np.linalg.norm(f)
            if (modulo_f  > self.temperatura):
                f = (f / modulo_f) * self.temperatura
                accum[node] = f

            self.posiciones[node] = self.posiciones[node] + accum[node]

    def compute_gravity_forces(self, accum):
        if(self.verbose):
            print("Se está sacando la fuerza de gravedad.")

        menor_fuerza = np.linalg.norm(accum[self.grafo[0][0]])
        for node in self.grafo[0]:
            otra_fuerza = np.linalg.norm(accum[node])
            if(menor_fuerza > otra_fuerza):
                menor_fuerza = otra_fuerza

        menor_fuerza /= 10 
        for node in self.grafo[0]:
            vector_gravedad = self.centro_pantalla - self.posiciones[node]
            vector_gravedad_con_modulo_especifico = (vector_gravedad / (np.linalg.norm(vector_gravedad))) * menor_fuerza
            accum[node] = accum[node] + vector_gravedad_con_modulo_especifico

    def fix_border_case(self):
        errors = True

        while errors:
            errors = False
            forces = self.initialize_accumulators

            for v in self.grafo[0]:
                for u in self.grafo[0]:
                    if v != u:
                        distance = np.linalg.norm(self.posiciones[u] - self.posiciones[v])

                        if distance <= EPSILON:
                            if(self.verbose):
                                print("El vértice %s y el vértice %s están muy juntos, por lo tanto, se están actualizando sus respectivas coordenadas.", u, v)

                            f = np.random.uniform(-1, 1, (1, 2))
                            f = (f / (np.linalg.norm(f))) * CONSTANTE_ESPARCIMIENTO
                            forces[u] = f
                            forces[v] = -1 * f
                            errors = True

            self.update_positions(forces)

    def fix_out_grafic(self, vertex):
        if(vertex[0] > LARGO/2):
            vertex[0] = LARGO/2
        if(vertex[0] < -LARGO/2):
            vertex[0] = -LARGO/2
        if(vertex[1] > ALTO/2):
            vertex[1] = ALTO/2
        if(vertex[1] < -ALTO/2):
            vertex[1] = -ALTO/2
        return vertex

    def grafic(self):
        if(self.verbose):
            print("Se está graficando el grafo.")

        self.setear_ejes()
        for u, v in self.grafo[1]:
            vert1 = self.fix_out_grafic(self.posiciones[u].tolist())
            vert2 = self.fix_out_grafic(self.posiciones[v].tolist())
            plt.plot([vert1[0], vert2[0]], [vert1[1], vert2[1]], marker='o')

    def reset_grafic(self):
        plt.draw()
        plt.pause(0.2)
        plt.clf()

    def step(self):
        self.fix_border_case()
        accum = self.initialize_accumulators
        self.compute_attraction_forces(accum)
        self.compute_repulsion_forces(accum)
        self.compute_gravity_forces(accum)
        self.update_positions(accum)
        self.update_temperature()

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        iteraciones = 0
        for k in range(1, self.iters):
            iteraciones += 1
            self.step()
            if(iteraciones == self.refresh):
                self.grafic()
                self.reset_grafic()
                iteraciones = 0

        if(self.refresh == 0):
            self.grafic()
            plt.show()

        pass

def lee_grafo_archivo(file_path):
    vertices = []
    aristas = []
    f = open(file_path, 'r')
    cant = int(f.readline())

    for i in range(cant):
        vertices += [f.readline()[:-1]]

    linea = f.readline()
    while linea:
        aux = linea.split()
        arista = (aux[0], aux[1])
        aristas += [arista]
        linea = f.readline()
    return (vertices, aristas)

def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=50
    )

    parser.add_argument(
        '--refresh',
        type=int,
        help='Cada cuantas iteraciones mostrar el nuevo grafo',
        default=1
    )

    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    grafo = lee_grafo_archivo(args.file_name)

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo,
        iters = args.iters,
        refresh = args.refresh,
        verbose = args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
