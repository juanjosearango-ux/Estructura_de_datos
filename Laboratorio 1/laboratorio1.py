import os
import struct
import time

FILAS = 100000
COLUMNAS = 100000
BYTES_POR_FILA = COLUMNAS // 8  # 12,500 bytes
NOMBRE_ARCHIVO = "matriz.bin"
MAGIC = b"MTX1"  # Identificador de formato (4 bytes)

def escribir_header(f, n_filas, n_columnas):
    """
    Escribe un header autodescriptivo de 12 bytes al inicio del archivo:
    - 4 bytes: Magic Number ('MTX1')
    - 4 bytes: Filas (uint32)
    - 4 bytes: Columnas (uint32)
    """
    header = struct.pack("<4sII", MAGIC, n_filas, n_columnas)
    f.write(header)
    return len(header)

def generar_matriz():
    print("--> Generando matriz de 100,000 x 100,000 en disco...")
    tiempo_inicio = time.time()
    
    # Fila de ceros empaquetada (12,500 bytes representativos)
    fila_buffer = bytes(BYTES_POR_FILA)
    
    with open(NOMBRE_ARCHIVO, "wb") as f:
        header_size = escribir_header(f, FILAS, COLUMNAS)
        
        # Escritura por bloques
        for i in range(0, FILAS, 10000):
            for _ in range(10000):
                f.write(fila_buffer)
            print(f"Progreso: {i + 10000}/{FILAS} filas escritas")

    tiempo_fin = time.time()
    tamano_bytes = os.path.getsize(NOMBRE_ARCHIVO)
    
    print(f"\nMatriz creada exitosamente.")
    print(f"Header: {header_size} bytes")
    print(f"Tiempo total: {tiempo_fin - tiempo_inicio:.2f} segundos")
    print(f"Tamaño real en disco: {tamano_bytes / (1024**3):.3f} GB ({tamano_bytes:,} bytes)")

if __name__ == "__main__":
    generar_matriz()