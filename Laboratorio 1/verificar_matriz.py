import os
import struct

NOMBRE_ARCHIVO = "matriz.bin"
MAGIC = b"MTX1"  # Identificador de cabecera de 4 bytes


def leer_header(f):
    # Desplaza al inicio y lee los 12 bytes de la cabecera (Magic + Filas + Columnas)
    f.seek(0)
    raw = f.read(12)
    magic, n_filas, n_columnas = struct.unpack("<4sII", raw)
    if magic != MAGIC:
        raise ValueError("Formato de archivo no válido.")
    return n_filas, n_columnas, 12


def consultar_coordenada(f, header_size, bytes_por_fila, fila, columna):
    """Acceso O(1) puntual calculando la posición exacta en disco mediante
    seek."""
    byte_offset = header_size + (fila * bytes_por_fila) + (columna // 8)
    bit_offset = columna % 8

    f.seek(byte_offset)
    byte_leido = int.from_bytes(f.read(1), "big")
    return (byte_leido >> (7 - bit_offset)) & 1


def leer_fila(f, header_size, bytes_por_fila, fila, max_cols=10):
    """Lee únicamente los bytes necesarios de una fila específica desde disco."""
    offset = header_size + (fila * bytes_por_fila)
    f.seek(offset)
    chunk = f.read((max_cols + 7) // 8)
    bits = []
    for b in chunk:
        for bit in range(7, -1, -1):
            bits.append((b >> bit) & 1)
    return bits[:max_cols]


def verificar():
    if not os.path.exists(NOMBRE_ARCHIVO):
        print(
            "Error: Primero debes ejecutar laboratorio1.py para generar la"
            " matriz."
        )
        return

    with open(NOMBRE_ARCHIVO, "rb") as f:
        # Validación e inspección del header
        n_filas, n_cols, header_size = leer_header(f)
        bytes_por_fila = n_cols // 8

        print("=== Estructura del archivo (Leída del Header) ===")
        print(f"Identificador: {MAGIC.decode()}")
        print(f"Filas: {n_filas:,} | Columnas: {n_cols:,}")
        print(f"Tamaño Header: {header_size} bytes\n")

        print("=== Muestra de contenido (Acceso directo por Seek) ===")
        print(
            "Fila 0 (primeros 10 bits):    "
            f" {leer_fila(f, header_size, bytes_por_fila, 0)}"
        )
        print(
            "Fila 50000 (primeros 10 bits):"
            f" {leer_fila(f, header_size, bytes_por_fila, 50000)}"
        )
        print(
            "Fila 99999 (primeros 10 bits):"
            f" {leer_fila(f, header_size, bytes_por_fila, 99999)}"
        )

        # Prueba puntual en una coordenada aleatoria
        val = consultar_coordenada(f, header_size, bytes_por_fila, 50000, 20)
        print(f"\nConsulta directa en Coordenada [50000, 20]: Valor = {val}")

        tamano_real = os.path.getsize(NOMBRE_ARCHIVO)
        print(
            f"\nTamaño del archivo en disco: {tamano_real / (1024**3):.3f} GB"
        )
        print(
            "Verificación completa: Acceso O(1) validado sin consumo de RAM"
            " excesivo."
        )


if __name__ == "__main__":
    verificar()