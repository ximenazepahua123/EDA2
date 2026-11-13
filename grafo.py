# grafo.py
from collections import deque

# Grafo representativo de la sucursal OXXO
GRAFO_OXXO = {
    "Caja": ["Bebidas", "Snacks"],
    "Bebidas": ["Caja", "Dulces", "Higiene"],
    "Snacks": ["Caja", "Dulces", "Limpieza"],
    "Dulces": ["Bebidas", "Snacks", "Higiene"],
    "Higiene": ["Bebidas", "Dulces", "Limpieza"],
    "Limpieza": ["Snacks", "Higiene"]
}

def bfs_ruta_corta(grafo, inicio, destino):
    """
    Realiza un recorrido Breadth-First Search (BFS) para encontrar 
    la ruta más corta entre una sección de origen y un destino en el OXXO.
    """
    # Validamos con normalización básica (capitalizando por si el usuario escribe en minúsculas)
    inicio = inicio.strip().title()
    destino = destino.strip().title()

    if inicio not in grafo or destino not in grafo:
        return None

    cola = deque([[inicio]])
    visitados = {inicio}

    while cola:
        ruta = cola.popleft()
        actual = ruta[-1]

        if actual == destino:
            return ruta

        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                nueva_ruta = ruta + [vecino]
                cola.append(nueva_ruta)

    return None