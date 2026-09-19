from merkle import crear_merkle_arbol

txs = ["Juan paga a Jose 10", "Pedro paga a Maria 5", "Maria paga a Mateo 12", "Mateo paga a Ana 2", "Ana paga a Juan 8"]
raiz, niveles = crear_merkle_arbol(txs)

print("Arbol por niveles:")
for i, nivel in enumerate(niveles):
    print(f"Nivel {i}:")
    for h in nivel:
        print(" ", h[:10])

print("\nTransacciones:")
print(txs)