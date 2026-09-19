Laboratorio 2: Árbol de Merkle

Estudiante: Juan José Arango Figueroa  
Curso: Estructuras de Datos  

# Descripción
Este proyecto contiene la implementación de un Árbol de Merkle en Python utilizando la librería hashlib para generar hashes SHA-256. Se construyen los niveles del árbol a partir de un arreglo de transacciones, gestionando casos impares mediante la duplicación del último nodo, e incluye funciones para generar y verificar pruebas de inclusión (Merkle Proofs).

# Archivos del Repositorio
* merkle.py: Código principal con las funciones de hashing y construcción del árbol (sha256, crear_merkle_arbol, obtener_prueba, verificar_prueba), junto con el experimento de 5 puntos del laboratorio.
* diagrama.py: Script auxiliar que importa crear_merkle_arbol desde merkle.py para visualizar en consola los hashes truncados por cada nivel del árbol.

# Instrucciones de Ejecución
Para ejecutar el programa principal y ver la verificación de pruebas en consola:
python merkle.py

Para visualizar la estructura del árbol por niveles:
python diagrama.py

# Declaración de Asistencia de IA
En cumplimiento del Código de Honor y las políticas de integridad académica de la asignatura, declaro el uso de herramientas de Inteligencia Artificial únicamente como apoyo en la redacción de la documentación en formato Markdown y en la organización del formato visual de las salidas en consola. La lógica del algoritmo, las funciones del árbol y los experimentos presentados fueron implementados por mi.
