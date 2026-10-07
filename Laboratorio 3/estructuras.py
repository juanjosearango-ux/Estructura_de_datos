# 1. LISTA SECUENCIAL
def buscar_en_lista(lista, id_buscar):
    for est in lista:
        if est['id'] == id_buscar:
            return est
    return None

# 2. ÁRBOL BINARIO DE BÚSQUEDA (ABB)
class NodoABB:
    def __init__(self, estudiante):
        self.id = estudiante['id']
        self.datos = estudiante
        self.izquierda = None
        self.derecha = None

class ArbolABB:
    def __init__(self):
        self.raiz = None

    # Insertar estudiante
    def insertar(self, estudiante):
        nuevo = NodoABB(estudiante)
        if self.raiz is None:
            self.raiz = nuevo
            return
        
        actual = self.raiz
        while True:
            if nuevo.id < actual.id:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    break
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    break
                actual = actual.derecha

    # Buscar estudiante por ID
    def buscar(self, id_buscar):
        actual = self.raiz
        while actual:
            if id_buscar == actual.id:
                return actual.datos
            elif id_buscar < actual.id:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

# 3. ÁRBOL B+
class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []

class ArbolBPlus:
    def __init__(self, orden=4):
        self.raiz = NodoBPlus(es_hoja=True)
        self.orden = orden

    # Buscar ID recorriendo hasta la hoja
    def buscar(self, id_buscar):
        actual = self.raiz
        while not actual.es_hoja:
            i = 0
            while i < len(actual.claves) and id_buscar >= actual.claves[i]:
                i += 1
            actual = actual.hijos[i]
        
        for i, k in enumerate(actual.claves):
            if k == id_buscar:
                return actual.hijos[i]
        return None

    # Inserción simplificada
    def insertar(self, estudiante):
        actual = self.raiz
        while not actual.es_hoja:
            i = 0
            while i < len(actual.claves) and estudiante['id'] >= actual.claves[i]:
                i += 1
            actual = actual.hijos[i]
        
        actual.claves.append(estudiante['id'])
        actual.hijos.append(estudiante)
        combinado = sorted(zip(actual.claves, actual.hijos), key=lambda x: x[0])
        actual.claves = [x[0] for x in combinado]
        actual.hijos = [x[1] for x in combinado]