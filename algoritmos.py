
def quick_sort_precio(productos, ascendente=True):
    """Algoritmo Quick Sort aplicado al catálogo por precio."""
    if len(productos) <= 1:
        return productos

    pivote = productos[len(productos) // 2]
    izquierda, centro, derecha = [], [], []

    for p in productos:
        if p["precio"] == pivote["precio"]:
            centro.append(p)
        elif ascendente:
            if p["precio"] < pivote["precio"]:
                izquierda.append(p)
            else:
                derecha.append(p)
        else:
            if p["precio"] > pivote["precio"]:
                izquierda.append(p)
            else:
                derecha.append(p)

    return quick_sort_precio(izquierda, ascendente) + centro + quick_sort_precio(derecha, ascendente)

def buscar_producto_por_id(productos, id_buscado):
    """Búsqueda secuencial por ID (Clave)."""
    for p in productos:
        if p["id"] == id_buscado:
            return p
    return None

def busqueda_lineal_nombre(productos, nombre_buscado):
    """Búsqueda lineal por coincidencia en el nombre del producto."""
    resultados = []
    nombre_buscado = nombre_buscado.lower()
    for p in productos:
        if nombre_buscado in p["nombre"].lower():
            resultados.append(p)
    return resultados

def busqueda_binaria_precio(productos, precio_buscado):
    """
    Búsqueda binaria por precio. 
    Requiere que la lista esté previamente ordenada por precio de menor a mayor.
    Devuelve una lista con todos los productos que coincidan con ese precio.
    """
    inicio = 0
    fin = len(productos) - 1
    resultados = []

    while inicio <= fin:
        medio = (inicio + fin) // 2
        
        # Si encontramos el precio exacto
        if productos[medio]["precio"] == precio_buscado:
            # Expandimos hacia la izquierda para buscar precios idénticos
            i = medio
            while i >= 0 and productos[i]["precio"] == precio_buscado:
                resultados.append(productos[i])
                i -= 1
            
            # Expandimos hacia la derecha para buscar precios idénticos
            i = medio + 1
            while i < len(productos) and productos[i]["precio"] == precio_buscado:
                resultados.append(productos[i])
                i += 1
                
            return resultados
        
        # Si el precio del medio es menor, buscamos en la mitad derecha
        elif productos[medio]["precio"] < precio_buscado:
            inicio = medio + 1
        # Si es mayor, buscamos en la mitad izquierda
        else:
            fin = medio - 1
            
    return resultados # Retorna lista vacía si no encuentra nada