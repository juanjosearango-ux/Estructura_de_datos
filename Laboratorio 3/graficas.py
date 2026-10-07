import csv
import matplotlib.pyplot as plt

# Leer datos de resultados.csv
datos_csv = []
with open("resultados.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        datos_csv.append(row)

# 1. GRAFICA 1: Escalabilidad N (Caso Aleatorio vs Peor Caso)
N_aleat, busq_lista_aleat, busq_abb_aleat, busq_bplus_aleat = [], [], [], []
N_orden, busq_lista_orden, busq_abb_orden, busq_bplus_orden = [], [], [], []

for d in datos_csv:
    if d["Tipo"] == "Escalabilidad_N_Aleatorio":
        N_aleat.append(int(d["N"]))
        busq_lista_aleat.append(float(d["busq_lista_mu"]))
        busq_abb_aleat.append(float(d["busq_abb_mu"]))
        busq_bplus_aleat.append(float(d["busq_bplus_mu"]))
    elif d["Tipo"] == "Escalabilidad_N_Ordenado":
        N_orden.append(int(d["N"]))
        busq_lista_orden.append(float(d["busq_lista_mu"]))
        busq_abb_orden.append(float(d["busq_abb_mu"]))
        busq_bplus_orden.append(float(d["busq_bplus_mu"]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Inserción Aleatoria
ax1.plot(N_aleat, busq_lista_aleat, 'r-o', linewidth=2, label='Lista O(N)')
ax1.plot(N_aleat, busq_abb_aleat, 'b-s', linewidth=2, label='ABB O(log N)')
ax1.plot(N_aleat, busq_bplus_aleat, 'g-^', linewidth=2, label='B+ O(log N)')
ax1.set_yscale('log')
ax1.set_title('Caso Promedio (Inserción Aleatoria)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Tamaño de Entrada N (Estudiantes)')
ax1.set_ylabel('Tiempo Búsqueda (s) [Escala Logarítmica]')
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend()

# Subplot 2: Inserción Ordenada
ax2.plot(N_orden, busq_lista_orden, 'r-o', linewidth=2, label='Lista O(N)')
ax2.plot(N_orden, busq_abb_orden, 'b-s', linewidth=2, label='ABB O(N) Degenerado')
ax2.plot(N_orden, busq_bplus_orden, 'g-^', linewidth=2, label='B+ O(log N)')
ax2.set_yscale('log')
ax2.set_title('Peor Caso (Inserción Ordenada)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Tamaño de Entrada N (Estudiantes)')
ax2.set_ylabel('Tiempo Búsqueda (s) [Escala Logarítmica]')
ax2.grid(True, which="both", ls="--", alpha=0.5)
ax2.legend()

plt.tight_layout()
plt.savefig('grafica_escalabilidad_N.png', dpi=300)
print(" Gráfica 'grafica_escalabilidad_N.png' actualizada.")

# 2. GRAFICA 2: Variación de M con Escala Logarítmica
M_vals, busq_l_M, busq_abb_M, busq_bp_M = [], [], [], []
for d in datos_csv:
    if d["Tipo"] == "Variacion_M":
        M_vals.append(int(d["M"]))
        busq_l_M.append(float(d["busq_lista_mu"]))
        busq_abb_M.append(float(d["busq_abb_mu"]))
        busq_bp_M.append(float(d["busq_bplus_mu"]))

plt.figure(figsize=(8, 5))
plt.plot(M_vals, busq_l_M, 'r-o', linewidth=2, label='Lista O(M*N)')
plt.plot(M_vals, busq_abb_M, 'b-s', linewidth=2, label='ABB O(M*log N)')
plt.plot(M_vals, busq_bp_M, 'g-^', linewidth=2, label='B+ O(M*log N)')
plt.yscale('log')  # Escala logarítmica para ver la diferencia real
plt.title('Impacto de Variar Operaciones M (N=10,000 Fijo)', fontsize=12, fontweight='bold')
plt.xlabel('Número de Búsquedas M')
plt.ylabel('Tiempo total de Búsqueda (s) [Escala Log]')
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('grafica_variacion_M.png', dpi=300)
print(" Gráfica 'grafica_variacion_M.png' actualizada.")