import time
import random
import math
from Quadtreetree import Rectangle, Quadtree

def generar_puntos(n):
    # Genera n puntos aleatorios dentro del área de la ciudad (0 a 10000 metros)
    return [(random.uniform(0, 10000), random.uniform(0, 10000)) for _ in range(n)]

def fuerza_bruta_range(puntos, centro, radio):
    # Recorre toda la lista evaluando la distancia euclidiana
    res = []
    for p in puntos:
        if math.hypot(p[0] - centro[0], p[1] - centro[1]) <= radio:
            res.append(p)
    return res

def correr_analisis():
    tamanios = [500, 1000, 2500, 5000, 7500, 10000]
    radio = 500
    punto_prueba = (5000, 5000)
    
    print("N_puntos | Fuerza_Bruta(s) | Quadtree(s)   | Mas_rapido")
    print("-" * 50)

    for n in tamanios:
        puntos = generar_puntos(n)
        
        # Construimos el Quadtree para este conjunto de datos
        boundary = Rectangle(5000, 5000, 5000, 5000)
        qtree = Quadtree(boundary, capacity=4)
        for p in puntos:
            qtree.insert(p)
            
        # Medimos fuerza bruta (promediando varias corridas para evitar ruido de la CPU)
        t0 = time.perf_counter()
        for _ in range(5):
            fuerza_bruta_range(puntos, punto_prueba, radio)
        t_fb = (time.perf_counter() - t0) / 5

        # Medimos Quadtree
        range_box = Rectangle(punto_prueba[0], punto_prueba[1], radio, radio)
        t0 = time.perf_counter()
        for _ in range(5):
            res_qt = []
            qtree.query_range(range_box, res_qt)
        t_qt = (time.perf_counter() - t0) / 5

        ganador = "Quadtree" if t_qt < t_fb else "Fuerza Bruta"
        print(f"{n:<8} | {t_fb:<14.6f} | {t_qt:<13.6f} | {ganador}")

if __name__ == "__main__":
    correr_analisis()