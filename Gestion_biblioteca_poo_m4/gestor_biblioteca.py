import json
import os

NOMBRE_ARCHIVO = 'biblioteca.txt'

class Libro:
    def __init__(self, titulo, autor, anio_publicacion, estado="Disponible"):
        self._titulo = titulo
        self._autor = autor
        self._anio_publicacion = anio_publicacion
        self._estado = estado  
    
    @property
    def titulo(self):
        return self._titulo
    
    @property
    def autor(self):
        return self._autor
        
    @property
    def anio_publicacion(self):
        return self._anio_publicacion
        
    @property
    def estado(self):
        return self._estado

    @titulo.setter
    def titulo(self, nuevo_titulo):
        self._titulo = nuevo_titulo
        
    @estado.setter
    def estado(self, nuevo_estado):
        if nuevo_estado in ["Disponible", "Prestado"]:
            self._estado = nuevo_estado
        else:
            raise ValueError("Estado inválido. Debe ser 'Disponible' o 'Prestado'.")

    def to_dict(self):
        return {
            "tipo": "Libro",
            "titulo": self._titulo,
            "autor": self._autor,
            "anio_publicacion": self._anio_publicacion,
            "estado": self._estado
        }

    def __str__(self):
        return f"Título: {self._titulo}, Autor: {self._autor}, Año: {self._anio_publicacion}, Estado: {self._estado}"


class LibroDigital(Libro):
    def __init__(self, titulo, autor, anio_publicacion, formato, estado="Disponible"):
        super().__init__(titulo, autor, anio_publicacion, estado)
        self._formato = formato
    
    @property
    def formato(self):
        return self._formato

    @formato.setter
    def formato(self, nuevo_formato):
        self._formato = nuevo_formato

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Formato: {self._formato}"

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "LibroDigital"
        data["formato"] = self._formato
        return data


class Biblioteca:
    def __init__(self):
        self._libros = []
        self._cargar_libros()

    def _cargar_libros(self):
        if not os.path.exists(NOMBRE_ARCHIVO):
            print(f"INFO: Archivo '{NOMBRE_ARCHIVO}' no encontrado. Iniciando biblioteca vacía.")
            return

        try:
            with open(NOMBRE_ARCHIVO, 'r') as f:
                for linea in f:
                    if not linea.strip():
                        continue
                    data = json.loads(linea)

                    if data.get("tipo") == "LibroDigital":
                        libro = LibroDigital(
                            data["titulo"], 
                            data["autor"], 
                            data["anio_publicacion"], 
                            data["formato"],
                            data["estado"]
                        )
                    else:
                        libro = Libro(
                            data["titulo"], 
                            data["autor"], 
                            data["anio_publicacion"], 
                            data["estado"]
                        )
                    self._libros.append(libro)

            print(f"INFO: Se cargaron {len(self._libros)} libros desde el archivo.")

        except Exception as e:
            print(f"ERROR al cargar libros: {e}")

    def guardar_libros(self):
        try:
            with open(NOMBRE_ARCHIVO, 'w') as f:
                for libro in self._libros:
                    f.write(json.dumps(libro.to_dict()) + '\n')
            print(f"INFO: Se guardaron {len(self._libros)} libros en '{NOMBRE_ARCHIVO}'.")
        except Exception as e:
            print(f"ERROR: No se pudieron guardar los libros: {e}")

    def agregar_libro(self, libro):
        if any(l.titulo.lower() == libro.titulo.lower() for l in self._libros):
            print(f"ERROR: Ya existe un libro con el título '{libro.titulo}'.")
            return
        self._libros.append(libro)
        print(f"ÉXITO: Libro '{libro.titulo}' agregado.")

    def eliminar_libro(self, titulo):
        titulo = titulo.lower()
        libro_a_eliminar = self.buscar_libro(titulo, exacto=True)

        if not libro_a_eliminar:
            raise IndexError(f"ERROR: No se encontró ningún libro con el título exacto '{titulo}'.")
        
        self._libros.remove(libro_a_eliminar)
        print(f"ÉXITO: Libro '{libro_a_eliminar.titulo}' eliminado.")

    def buscar_libro(self, titulo, exacto=False):
        titulo_norm = titulo.lower()
        
        if exacto:
            return next((libro for libro in self._libros if libro.titulo.lower() == titulo_norm), None)

        return [libro for libro in self._libros if titulo_norm in libro.titulo.lower()]

    def listar_disponibles(self):
        disponibles = [libro for libro in self._libros if libro.estado == "Disponible"]
        if not disponibles:
            print("\n--- No hay libros disponibles. ---")
            return
        
        print("\n--- Libros Disponibles ---")
        for i, libro in enumerate(disponibles, 1):
            print(f"{i}. {libro}")
        print("-" * 30)
        return disponibles

    def marcar_prestado(self, titulo):
        libro = self.buscar_libro(titulo, exacto=True)

        if not libro:
            raise IndexError(f"ERROR: No se encontró el libro con título exacto '{titulo}'.")
        
        if libro.estado == "Prestado":
            raise ValueError(f"ERROR: El libro '{libro.titulo}' ya está prestado.")

        libro.estado = "Prestado"
        print(f"ÉXITO: Libro '{libro.titulo}' marcado como Prestado.")

    def devolver_libro(self, titulo):
        libro = self.buscar_libro(titulo, exacto=True)

        if not libro:
            raise IndexError(f"ERROR: No se encontró el libro con título exacto '{titulo}'.")
        
        if libro.estado == "Disponible":
            print(f"INFO: El libro '{libro.titulo}' ya está disponible.")
            return

        libro.estado = "Disponible"
        print(f"ÉXITO: Libro '{libro.titulo}' devuelto y disponible.")


def mostrar_menu():
    print("\n--- Gestor de Biblioteca ---")
    print("1. Agregar libro")
    print("2. Eliminar libro")
    print("3. Ver todos los libros disponibles")
    print("4. Buscar libro por título")
    print("5. Marcar libro como prestado")
    print("6. Devolver libro")
    print("7. Salir")
    return input("Elige una opción: ")

def main():
    biblioteca = Biblioteca()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            print("\n--- Agregar Libro ---")
            titulo = input("Título: ")
            autor = input("Autor: ")
            anio = input("Año de publicación: ")
            tipo = input("¿Es digital? (s/n): ").lower()
            
            if tipo == 's':
                formato = input("Formato (PDF, ePub): ")
                nuevo_libro = LibroDigital(titulo, autor, anio, formato)
            else:
                nuevo_libro = Libro(titulo, autor, anio)
                
            biblioteca.agregar_libro(nuevo_libro)

        elif opcion == '2':
            print("\n--- Eliminar Libro ---")
            titulo = input("Título del libro a eliminar: ")
            try:
                biblioteca.eliminar_libro(titulo)
            except IndexError as e:
                print(e)
                
        elif opcion == '3':
            biblioteca.listar_disponibles()
            
        elif opcion == '4':
            print("\n--- Buscar Libro ---")
            titulo = input("Introduce el título o parte del título: ")
            resultados = biblioteca.buscar_libro(titulo, exacto=False)
            if resultados:
                print("\n--- Resultados de Búsqueda ---")
                for i, libro in enumerate(resultados, 1):
                    print(f"{i}. {libro}")
                print("-" * 30)
            else:
                print("INFO: No se encontraron coincidencias.")

        elif opcion == '5':
            print("\n--- Marcar Libro Prestado ---")
            titulo = input("Título del libro a prestar: ")
            try:
                biblioteca.marcar_prestado(titulo)
            except (IndexError, ValueError) as e:
                print(e)

        elif opcion == '6':
            print("\n--- Devolver Libro ---")
            titulo = input("Título del libro a devolver: ")
            try:
                biblioteca.devolver_libro(titulo)
            except IndexError as e:
                print(e)

        elif opcion == '7':
            biblioteca.guardar_libros()
            print("¡Gracias por usar el Gestor de Biblioteca! Los cambios han sido guardados.")
            break
        
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
