import random
import time
import statistics
import csv
from estructuras import buscar_en_lista, ArbolABB, ArbolBPlus

nombres = ["Ana", "Carlos", "María", "Juan", "Pedro", "Sofia", "Luis", "Elena"]

def generar_estudiantes(n):
    ids = random.sample(range(10000, 9999999), n)
    return [{"id": idx, "nombre": random.choice(nombres), "edad": random.randint(18, 25), "promedio": round(random.uniform(2.5, 5.0), 2)} for idx in ids]

def medicion_experimento(datos, ordenados=False, M=1000, repeticiones=5):
    if ordenados:
        datos = sorted(datos, key=lambda x: x['id'])

    t_const_lista, t_const_abb, t_const_bplus = [], [], []
    t_busq_lista, t_busq_abb, t_busq_bplus = [], [], []

    for _ in range(repeticiones):
        ids_a_buscar = [random.choice(datos)['id'] for _ in range(M)]

        # CONSTRUCCIÓN 
        # Lista
        t0 = time.perf_counter()
        lista_est = list(datos)
        t_const_lista.append(time.perf_counter() - t0)

        # ABB
        t0 = time.perf_counter()
        abb = ArbolABB()
        for est in datos:
            abb.insertar(est)
        t_const_abb.append(time.perf_counter() - t0)

        # B+
        t0 = time.perf_counter()
        bplus = ArbolBPlus()
        for est in datos:
            bplus.insertar(est)
        t_const_bplus.append(time.perf_counter() - t0)

        # BÚSQUEDA
        # Lista
        t0 = time.perf_counter()
        for idx in ids_a_buscar:
            buscar_en_lista(lista_est, idx)
        t_busq_lista.append(time.perf_counter() - t0)

        # ABB
        t0 = time.perf_counter()
        for idx in ids_a_buscar:
            abb.buscar(idx)
        t_busq_abb.append(time.perf_counter() - t0)

        # B+
        t0 = time.perf_counter()
        for idx in ids_a_buscar:
            bplus.buscar(idx)
        t_busq_bplus.append(time.perf_counter() - t0)

    return {
        "const_lista_mu": statistics.mean(t_const_lista),
        "const_lista_std": statistics.stdev(t_const_lista) if len(t_const_lista) > 1 else 0,
        "const_abb_mu": statistics.mean(t_const_abb),
        "const_abb_std": statistics.stdev(t_const_abb) if len(t_const_abb) > 1 else 0,
        "const_bplus_mu": statistics.mean(t_const_bplus),
        "const_bplus_std": statistics.stdev(t_const_bplus) if len(t_const_bplus) > 1 else 0,
        "busq_lista_mu": statistics.mean(t_busq_lista),
        "busq_lista_std": statistics.stdev(t_busq_lista) if len(t_busq_lista) > 1 else 0,
        "busq_abb_mu": statistics.mean(t_busq_abb),
        "busq_abb_std": statistics.stdev(t_busq_abb) if len(t_busq_abb) > 1 else 0,
        "busq_bplus_mu": statistics.mean(t_busq_bplus),
        "busq_bplus_std": statistics.stdev(t_busq_bplus) if len(t_busq_bplus) > 1 else 0,
    }

# EXPERIMENTOS PRINCIPALES
resultados = []

# Experimento A: Variando N (N=1000, 5000, 10000, 15000, 20000), M=1000 Fijo
tamanos_N = [1000, 5000, 10000, 15000, 20000]
print("Iniciando Experimentos variando N...")

for N in tamanos_N:
    print(f"  -> Ejecutando para N={N} (Aleatorio y Ordenado)...")
    datos = generar_estudiantes(N)
    
    # Aleatorio
    res_aleat = medicion_experimento(datos, ordenados=False, M=1000, repeticiones=5)
    res_aleat.update({"Tipo": "Escalabilidad_N_Aleatorio", "N": N, "M": 1000})
    resultados.append(res_aleat)
    
    # Ordenado (Peor caso)
    res_orden = medicion_experimento(datos, ordenados=True, M=1000, repeticiones=5)
    res_orden.update({"Tipo": "Escalabilidad_N_Ordenado", "N": N, "M": 1000})
    resultados.append(res_orden)

# Experimento B: Variando M (M=100, 500, 1000, 2500, 5000), N=10000 Fijo
tamanos_M = [100, 500, 1000, 2500, 5000]
print("Iniciando Experimentos variando M (N=10000 Fijo)...")
datos_fijos = generar_estudiantes(10000)

for M in tamanos_M:
    print(f"  -> Ejecutando para M={M}...")
    res_M = medicion_experimento(datos_fijos, ordenados=False, M=M, repeticiones=5)
    res_M.update({"Tipo": "Variacion_M", "N": 10000, "M": M})
    resultados.append(res_M)

# Guardar resultados en CSV
with open("resultados.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
    writer.writeheader()
    writer.writerows(resultados)

print("\n¡Experimentos finalizados exitosamente! Datos guardados en 'resultados.csv'.")