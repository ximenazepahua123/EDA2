import os
import pickle

# Usamos una ruta relativa (el archivo se guardará en la misma carpeta del proyecto)
NOMBRE_ARCHIVO = "inventario_oxxo.pkl"

def cargar_inventario(productos_iniciales):
    """
    Carga el archivo al iniciar. Si no existe, lo crea por primera vez con los datos iniciales.
    Si hay un error de lectura, no sobrescribe nada por seguridad.
    """
    if os.path.exists(NOMBRE_ARCHIVO):
        try:
            with open(NOMBRE_ARCHIVO, "rb") as archivo:
                datos = pickle.load(archivo)
                if not datos:
                    print(" Advertencia: El archivo está vacío. Se usarán los datos por defecto.")
                    return productos_iniciales
                print(" Datos cargados correctamente desde el archivo.")
                return datos
        except Exception as e:
            print(f" Error al leer el archivo: {e}. No se sobrescribirán los datos iniciales.")
            return productos_iniciales
    else:
        # Si no existe, lo crea por primera vez con los 50 productos
        guardar_inventario(productos_iniciales)
        print(" Archivo creado por primera vez con los datos de prueba.")
        return productos_iniciales

def guardar_inventario(productos):
    """
    Guarda los cambios actuales en el archivo de forma segura.
    """
    try:
        with open(NOMBRE_ARCHIVO, "wb") as archivo:
            pickle.dump(productos, archivo) # o solo archivo
        print(" ¡Cambios guardados exitosamente en el archivo!")
    except Exception as e:
        print(f" Ocurrió un error al intentar guardar el archivo: {e}")