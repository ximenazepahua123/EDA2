# 1. Agregamos la importación de persistencia aquí arriba
from persistencia import cargar_inventario, guardar_inventario

from datos import CATALOGO_PRODUCTOS
from grafo import GRAFO_OXXO, bfs_ruta_corta 
from algoritmos import (
    quick_sort_precio,
    buscar_producto_por_id,
    busqueda_lineal_nombre,
    busqueda_binaria_precio
)

def mostrar_menu():
    print("\n========================================")
    print("        SISTEMA PUNTO DE VENTA - OXXO     ")
    print("========================================")
    print("1. Mostrar catálogo de productos")
    print("2. Ordenar catálogo por precio  Ascendente / Descendente")
    print("3. Buscar producto por ID")
    print("4. Buscar producto por Nombre ")#(Búsqueda Lineal)
    print("5. Buscar producto por Precio exacto ")#(Búsqueda Binaria)
    print("6. Simular recorrido de abastecimiento en Tienda ")#(Grafo BFS)
    print("7. Registrar venta / Actualizar stock (Guardar cambios)") #
    print("8. Agregar nuevo producto (Alta)") 
    print("9. Salir") # 

def ejecutar_sistema():
    catalogo_actual = cargar_inventario(CATALOGO_PRODUCTOS)

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print(f"\n--- CATÁLOGO DE PRODUCTOS ({len(catalogo_actual)} registros) ---")
            for p in catalogo_actual:
                print(f"ID: {p['id']} | {p['nombre']:<26} | Precio: ${p['precio']:<6.2f} | Stock: {p['stock']}")

        elif opcion == "2":
            sub_op = input("¿Desea orden ascendente (1) o descendente (2) con Quick Sort?: ").strip()
            if sub_op in ["1", "2"]:
                asc = True if sub_op == "1" else False
                catalogo_actual = quick_sort_precio(catalogo_actual, ascendente=asc)
                direccion = "MENOR a MAYOR" if asc else "MAYOR a MENOR"
                print(f"\nÉxito Catálogo ordenado por precio de {direccion} usando Quick Sort.")
                for p in catalogo_actual[:5]:
                    print(f" - {p['nombre']}: ${p['precio']:.2f}")
                print(f"(... y {len(catalogo_actual) - 5} registros más ordenados)")
            else:
                print("\nError Opción de ordenamiento no válida.")

        elif opcion == "3":
            try:
                id_input = int(input("Ingrese el ID del producto a buscar: "))
                resultado = buscar_producto_por_id(catalogo_actual, id_input)
                if resultado:
                    print(f"\nEncontrado ID: {resultado['id']} | {resultado['nombre']} | Precio: ${resultado['precio']:.2f} | Stock: {resultado['stock']}")
                else:
                    print("\nAviso La clave ingresada no existe en el sistema.")
            except ValueError:
                print("\nError Entrada inválida. Debe ingresar un número entero para el ID.")

        elif opcion == "4":
            nombre_input = input("Ingrese el nombre del producto a buscar: ").strip()
            resultados = busqueda_lineal_nombre(catalogo_actual, nombre_input)
            if resultados:
                print(f"\nEncontrado Se encontraron {len(resultados)} coincidencias:")
                for r in resultados:
                    print(f"ID: {r['id']} | {r['nombre']} | Precio: ${r['precio']:.2f} | Stock: {r['stock']}")
            else:
                print("\n[Aviso] No se encontraron productos con ese nombre.")

        elif opcion == "5":
            try:
                # La búsqueda binaria requiere que el catálogo esté ordenado previamente por precio de menor a mayor
                catalogo_ordenado = quick_sort_precio(catalogo_actual, ascendente=True)
                precio_input = float(input("Ingrese el precio exacto a buscar (Búsqueda Binaria): "))
                resultados = busqueda_binaria_precio(catalogo_ordenado, precio_input)
                if resultados:
                    print(f"\nEncontrado Productos con precio ${precio_input:.2f}:")
                    for r in resultados:
                        print(f"ID: {r['id']} | {r['nombre']} | Stock: {r['stock']}")
                else:
                    print("\nAviso No hay productos con ese precio exacto.")
            except ValueError:
                print("\nError Entrada inválida. Debe ingresar un valor numérico válido.")

        elif opcion == "6":
            print("\n=== BÚSQUEDA DE RUTA EN SUCURSAL OXXO (BFS) ===")
            print("Secciones disponibles en la tienda:")
            for seccion in GRAFO_OXXO:
                print(f" - {seccion}")

            inicio = input("\nIntroduce la sección de origen: ").strip()
            destino = input("Introduce la sección de destino: ").strip()

            ruta = bfs_ruta_corta(GRAFO_OXXO, inicio, destino)

            if ruta is None:
                print("\nAviso No se ha encontrado una ruta o las secciones ingresadas no son válidas.")
            else:
                print("\nÉxito Ruta más corta encontrada:")
                print(" -> ".join(ruta))
                print(f"Número de conexiones: {len(ruta) - 1}")

        # 3. NUEVA OPCIÓN: Simula la venta, actualiza el stock y guarda automáticamente en el archivo .pkl
        elif opcion == "7":
            print("\n=== REGISTRAR VENTA / ACTUALIZAR STOCK ===")
            try:
                id_venta = int(input("Ingrese el ID del producto vendido: "))
                encontrado = False
                for p in catalogo_actual:
                    if p['id'] == id_venta:
                        encontrado = True
                        if p['stock'] > 0:
                            p['stock'] -= 1  # Modificamos el campo stock (operación real)
                            print(f"¡Venta registrada con éxito! Nuevo stock de '{p['nombre']}': {p['stock']}")
                            # Guardamos los cambios inmediatamente en el archivo
                            guardar_inventario(catalogo_actual)
                        else:
                            print("\n Aviso: El producto está agotado (Stock en 0).")
                        break
                if not encontrado:
                    print("\n Aviso: No se encontró ningún producto con ese ID.")
            except ValueError:
                print("\nError: Debe ingresar un número entero válido para el ID.")

        elif opcion == "8":
            print("\n=== AGREGAR NUEVO PRODUCTO ===")
            try:
                nuevo_id = int(input("Ingrese el ID del nuevo producto: "))
                if any(p["id"] == nuevo_id for p in catalogo_actual):
                    print("\nAviso: Ya existe un producto con ese ID.")
                    continue

                nuevo_nombre = input("Ingrese el nombre del producto: ").strip()
                if not nuevo_nombre:
                    print("\nError: El nombre no puede estar vacío.")
                    continue

                nuevo_precio = float(input("Ingrese el precio: "))
                nuevo_stock = int(input("Ingrese el stock inicial: "))
                if nuevo_precio <= 0 or nuevo_stock < 0:
                    print("\nError: El precio debe ser mayor a 0 y el stock no puede ser negativo.")
                    continue

                catalogo_actual.append({
                    "id": nuevo_id,
                    "nombre": nuevo_nombre,
                    "precio": nuevo_precio,
                    "stock": nuevo_stock
                })
                guardar_inventario(catalogo_actual)
            except ValueError:
                print("\nError: Ingrese valores numéricos válidos para ID, precio y stock.")

        elif opcion == "9":
            print("\n¡Gracias por utilizar el sistema OXXO! Saliendo...")
            break
        else:
            print("\nError: Opción no válida. Intente de nuevo ingresando un número del 1 al 9.")
if __name__ == "__main__":
    ejecutar_sistema()