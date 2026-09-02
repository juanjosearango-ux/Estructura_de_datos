# Laboratorio 1: Matriz 100,000 x 100,000 en Disco

**Estudiante:** Juan José Arango Figueroa  
**Materia:** Laboratorio de Estructuras de Datos  

## Objetivo
Crear y manipular una matriz de $100,000 \times 100,000$ en disco duro resolviendo los problemas de consumo excesivo de RAM, escritura lenta a disco y lectura optimizada.

## Enfoque de la Solución

1. **Matriz Binaria Empaquetada:** Se empaquetan 8 valores lógicos por cada byte físico, reduciendo el tamaño en disco de ~10 GB a **1.16 GB / 1.25 GB** ($1,250,000,012$ bytes incluyendo header).
2. **Procesamiento por Bloques:** La matriz no se carga completa en RAM. Se genera y escribe iterativamente por bloques manteniendo el uso de memoria en un nivel mínimo e insignificante.
3. **Header Autodescriptivo (12 Bytes):** El archivo binario no es ciego. Incluye una cabecera con la estructura:
   * 4 bytes: Identificador de formato (`MTX1`).
   * 4 bytes: Número de filas (`uint32`).
   * 4 bytes: Número de columnas (`uint32`).
4. **Acceso Directo $O(1)$ sin Marcadores:** Como el tamaño por fila es fijo ($12,500$ bytes), la posición de cualquier fila/coordenada se calcula directamente mediante desplazamientos en disco (`seek`):
   $$\text{Posición Fila}(i) = \text{Header} + (i \times \text{Bytes por Fila})$$
    Esto evita escaneos secuenciales y no requiere marcadores de fin de fila.

## Archivos del Repositorio
* `laboratorio1.py`: Genera la matriz binaria empaquetada y escribe el header autodescriptivo en disco.
* `verificar_matriz.py`: Lee el header del archivo binario y realiza consultas arbitrarias por coordenadas sin cargar la matriz en RAM.
* `README.md`: Documentación detallada del proyecto.
* `.gitignore`: Configurado para ignorar la subida del archivo pesado `.bin` al control de versiones.

## Guía de Ejecución

```bash
python laboratorio1.py
python verificar_matriz.py