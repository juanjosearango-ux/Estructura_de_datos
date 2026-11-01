import math
import random
import matplotlib.pyplot as plt
from Quadtreetree import Rectangle, Quadtree

# Funciones auxiliares de fuerza bruta y generación para las pruebas
def generar_puntos(n):
    return [(random.uniform(0, 10000), random.uniform(0, 10000)) for _ in range(n)]

def fuerza_bruta_range(puntos, centro, radio):
    res = []
    for p in puntos:
        if math.hypot(p[0] - centro[0], p[1] - centro[1]) <= radio:
            res.append(p)
    return res

def fuerza_bruta_nearest(puntos, centro):
    mas_cercano = None
    min_dist = float('inf')
    for p in puntos:
        dist = math.hypot(p[0] - centro[0], p[1] - centro[1])
        if dist < min_dist:
            min_dist = dist
            mas_cercano = p
    return mas_cercano

def probar_funcionalidad():
    print("--- EJECUTANDO PRUEBAS UNITARIAS ---")
    
    rect = Rectangle(50, 50, 50, 50)
    assert rect.contains((50, 50)) == True, "Error: Debería contener el centro"
    assert rect.contains((150, 150)) == False, "Error: No debe contener puntos fuera"
    print("[OK] Pruebas de límites de rectángulo pasadas.")

    puntos_prueba = [(10, 10), (20, 20), (80, 80), (90, 90), (50, 50)]
    boundary = Rectangle(50, 50, 50, 50)
    qtree = Quadtree(boundary, capacity=2)
    
    for p in puntos_prueba:
        qtree.insert(p)
        
    range_box = Rectangle(15, 15, 15, 15)
    encontrados_qt = []
    qtree.query_range(range_box, encontrados_qt)
    
    encontrados_fb = fuerza_bruta_range(puntos_prueba, (15, 15), 15)
    
    assert sorted(encontrados_qt) == sorted(encontrados_fb), "Error en Range Search"
    print("[OK] Prueba de Range Search validada contra Fuerza Bruta.")

    objetivo = (18, 18)
    _, vecino_qt = qtree.query_nearest(objetivo)
    vecino_fb = fuerza_bruta_nearest(puntos_prueba, objetivo)
    
    assert vecino_qt == vecino_fb, "Error en vecino más cercano"
    print("[OK] Prueba de vecino más cercano validada.")

def generar_graficas_verificacion():
    print("\n--- GENERANDO GRÁFICAS DE VERIFICACIÓN VISUAL ---")
    
    n = 100
    puntos = generar_puntos(n)
    
    boundary = Rectangle(5000, 5000, 5000, 5000)
    qtree = Quadtree(boundary, capacity=4)
    for p in puntos:
        qtree.insert(p)
        
    centro_busqueda = (5000, 5000)
    radio = 1500
    range_box = Rectangle(centro_busqueda[0], centro_busqueda[1], radio, radio)
    
    puntos_en_rango = []
    qtree.query_range(range_box, puntos_en_rango)
    
    _, vecino_cercano = qtree.query_nearest(centro_busqueda)

    plt.figure(figsize=(8, 8))
    xs, ys = zip(*puntos)
    plt.scatter(xs, ys, color='blue', s=15, label='Puntos de entrega')
    
    if puntos_en_rango:
        rx, ry = zip(*puntos_en_rango)
        plt.scatter(rx, ry, color='green', s=40, label='En rango')
        
    rect_plot = plt.Rectangle((centro_busqueda[0] - radio, centro_busqueda[1] - radio), 
                              radio * 2, radio * 2, linewidth=1.5, edgecolor='red', facecolor='none', linestyle='--', label='Área de búsqueda')
    plt.gca().add_patch(rect_plot)
    
    plt.title('Verificación Visual: Range Search (Quadtree)')
    plt.xlabel('X (metros)')
    plt.ylabel('Y (metros)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('range_search_plot.png', dpi=300)
    plt.close()
    print("[OK] Gráfica 'range_search_plot.png' guardada con éxito.")

    plt.figure(figsize=(8, 8))
    plt.scatter(xs, ys, color='blue', s=15, label='Puntos de entrega')
    plt.scatter(centro_busqueda[0], centro_busqueda[1], color='orange', s=100, marker='X', label='Ubicación objetivo')
    
    if vecino_cercano:
        plt.scatter(vecino_cercano[0], vecino_cercano[1], color='red', s=80, marker='o', label='Más cercano')
        plt.plot([centro_busqueda[0], vecino_cercano[0]], 
                 [centro_busqueda[1], vecino_cercano[1]], 
                 color='red', linestyle=':')

    plt.title('Verificación Visual: Vecino Más Cercano')
    plt.xlabel('X (metros)')
    plt.ylabel('Y (metros)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('nearest_neighbor_plot.png', dpi=300)
    plt.close()
    print("[OK] Gráfica 'nearest_neighbor_plot.png' guardada con éxito.")

if __name__ == "__main__":
    probar_funcionalidad()
    generar_graficas_verificacion()