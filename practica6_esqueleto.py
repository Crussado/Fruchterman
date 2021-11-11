#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import matplotlib.pyplot as plt
import numpy as np
import random
import math

CONSTANTE_REPULSION = 0.1
CONSTANTE_ATRACCION = 5.0
CONSTANTE_ESPARCIMIENTO = 1

MAX_X = 100
MAX_Y = 100

class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        c1: constante de repulsión
        c2: constante de atracción
        verbose: si está encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        # Completar
        self.posiciones = self.coordenadas_aleatorias(self.grafo[0])
        self.fuerzas = {}

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2

        self.k = CONSTANTE_ESPARCIMIENTO * math.sqrt((MAX_X * MAX_Y)/len(self.grafo[0]))

    def coordenadas_aleatorias(self, vertices):
        posiciones = {}
        for v in vertices:
            posiciones[v] = np.array([random.randrange(0, MAX_X), random.randrange(0, MAX_Y)])
        return posiciones

    @property
    def initialize_accumulators(self):
        accum = {}
        for v in self.grafo[0]:
            accum[v] = np.array([0, 0])
        return accum

    def f_attraction(self, distance):
        return distance**2 / self.k

    def f_repulsion(self, distance):
        return self.k**2 / distance

    def compute_repulsion_forces(self, accum):
        for n_i in self.grafo[0]:
            for n_j in self.grafo[0]:
                if n_i != n_j:
                    distance = np.linalg.norm(self.posiciones[n_i] - self.posiciones[n_j])
                    mod_fa = self.f_repulsion(distance)
                    f = mod_fa * (self.posiciones[n_j] - self.posiciones[n_i]) / distance

                    accum[n_i] = accum[n_i] + f
                    accum[n_j] = accum[n_j] - f

    def compute_attraction_forces(self, accum):
        for n_i, n_j in self.grafo[1]:
            distance = np.linalg.norm(self.posiciones[n_i] - self.posiciones[n_j])
            mod_fa = self.f_attraction(distance)
            f = mod_fa * (self.posiciones[n_j] - self.posiciones[n_i]) / distance

            accum[n_i] = accum[n_i] + f
            accum[n_j] = accum[n_j] - f

    def update_positions(self, accum):
        for node in self.grafo[0]:
            self.posiciones[node] = self.posiciones[node] + accum[node]

    def step(self):
        accum = self.initialize_accumulators
        self.compute_attraction_forces(accum)
        self.compute_repulsion_forces(accum)
        self.update_positions(accum)

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        # for u, v in self.grafo[1]:
        #     vert1 = self.posiciones[u].tolist()
        #     vert2 = self.posiciones[v].tolist()
        #     plt.plot([vert1[0], vert2[0]], [vert1[1], vert2[1]], marker='o')
        # plt.show()

        for k in range(1, self.iters):
            self.step()

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

    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )

    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    grafo = lee_grafo_archivo(args.file_name)

    # Descomentar abajo para ver funcionamiento de argparse
    # print(args.verbose)
    # print(args.iters)
    # print(args.file_name)
    # print(args.temp)
    # return
    # TODO: Borrar antes de la entrega
    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo,  # TODO: Cambiar para usar grafo leido de archivo
        iters = args.iters,
        refresh = args.refresh,
        c1 = CONSTANTE_REPULSION,
        c2 = CONSTANTE_ATRACCION,
        verbose = args.verbose
    )
    
    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
