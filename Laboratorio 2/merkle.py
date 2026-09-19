import hashlib

def sha256(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def crear_merkle_arbol(transacciones):
    # Aqui generamos los hashes de las transacciones (en hojas)
    nivel_actual = []
    for tx in transacciones:
        nivel_actual.append(sha256(tx))
        
    niveles = [nivel_actual]
    
    # Subimos armando el arbol por niveles
    while len(nivel_actual) > 1:
        # Si la lista es impar, se duplica el ultimo nodo
        if len(nivel_actual) % 2 != 0:
            nivel_actual.append(nivel_actual[-1])
            
        sig_nivel = []
        for i in range(0, len(nivel_actual), 2):
            pareja = nivel_actual[i] + nivel_actual[i+1]
            sig_nivel.append(sha256(pareja))
            
        nivel_actual = sig_nivel
        niveles.append(nivel_actual)
        
    return niveles[-1][0], niveles

def obtener_prueba(indice, niveles):
    prueba = []
    idx = indice
    
    # Recorremos los niveles para guardar los hashes hermanos
    for nivel in niveles[:-1]:
        copia_nivel = list(nivel)
        if len(copia_nivel) % 2 != 0:
            copia_nivel.append(copia_nivel[-1])
            
        es_par = (idx % 2 == 0)
        idx_hermano = idx + 1 if es_par else idx - 1
        
        hermano = copia_nivel[idx_hermano]
        posicion = "derecha" if es_par else "izquierda"
        
        prueba.append((hermano, posicion))
        idx = idx // 2
        
    return prueba

def verificar_prueba(tx, prueba, raiz):
    hash_actual = sha256(tx)
    
    for hermano, posicion in prueba:
        if posicion == "derecha":
            combinado = hash_actual + hermano
        else:
            combinado = hermano + hash_actual
        hash_actual = sha256(combinado)
        
    return hash_actual == raiz

# EXPERIMENTO DEL LABORATORIO

if __name__ == "__main__":
    print("EXPERIMENTO ARBOL DE MERKLE")
    
    # 1. 5 transacciones simples
    txs = ["Juan paga a Jose 10", "Pedro paga a Maria 5", "Maria paga a Mateo 12", "Mateo paga a Ana 2", "Ana paga a Juan 8"]
    print("\n1. Transacciones iniciales (5):")
    print(txs)

    # 2. Construir arbol y mostrar Merkle Root
    raiz_original, niveles = crear_merkle_arbol(txs)
    print("\n2. Raiz del arbol (Merkle Root):")
    print(raiz_original)

    # 3. Modificar la transaccion 3 y verificar cambio de raiz
    txs_mod = list(txs)
    txs_mod[2] = "Maria paga a Mateo 100" # Se cambia el valor
    raiz_mod, _ = crear_merkle_arbol(txs_mod)
    print("\n3. Transaccion 3 modificada:", txs_mod[2])
    print("Nueva Merkle Root:", raiz_mod)
    print("¿La raiz cambio?:", "SI" if raiz_original != raiz_mod else "NO")

    # 4. Prueba de inclusion para la Transaccion 3 original (indice 2)
    idx = 2
    tx_probar = txs[idx]
    prueba_tx3 = obtener_prueba(idx, niveles)
    es_valida = verificar_prueba(tx_probar, prueba_tx3, raiz_original)
    print(f"\n4. Prueba de inclusion para '{tx_probar}':")
    print("Resultado de verificacion:", "VALIDA" if es_valida else "INVALIDA")

    # 5. Verificar con un dato falso (aca debe fallar)
    tx_falsa = "Maria paga a Mateo 999"
    es_falsa_valida = verificar_prueba(tx_falsa, prueba_tx3, raiz_original)
    print(f"\n5. Prueba con dato falso ('{tx_falsa}'):")
    print("Resultado de verificacion:", "VALIDA" if es_falsa_valida else "INVALIDA (Correcto)")