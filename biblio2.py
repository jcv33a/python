import json
import os

class Libro:
    ARCHIVO_DATOS = 'biblioteca.json'
    libros = []

    def __init__(self, titulo: str, autor: str, isbn: str, disponible: bool = True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible
        Libro.libros.append(self)
        Libro.guardar_datos()  # Guardar al crear un libro

    @classmethod
    def cargar_datos(cls):
        """Carga los libros desde el archivo JSON al iniciar el programa"""
        if os.path.exists(cls.ARCHIVO_DATOS) and os.path.getsize(cls.ARCHIVO_DATOS) > 0:
            with open(cls.ARCHIVO_DATOS, 'r') as f:
                datos = json.load(f)
                for libro_data in datos:
                    cls(
                        titulo=libro_data['titulo'],
                        autor=libro_data['autor'],
                        isbn=libro_data['isbn'],
                        disponible=libro_data['disponible']
                    )
        else:
            cls.libros = []

    @classmethod
    def guardar_datos(cls):
        """Guarda los libros en el archivo JSON"""
        datos = []
        for libro in cls.libros:
            datos.append({
                'titulo': libro.titulo,
                'autor': libro.autor,
                'isbn': libro.isbn,
                'disponible': libro.disponible
            })
        with open(cls.ARCHIVO_DATOS, 'w') as f:
            json.dump(datos, f, indent=2)

    @classmethod
    def agregar(cls):
        """Agrega un libro con validación de ISBN único"""
        titulo = input("Ingrese el título: ")
        autor = input("Ingrese el autor: ")
        isbn = input("Ingrese el ISBN: ").strip()
        
        if cls.buscar(isbn):
            print(f"❌ Ya existe un libro con el ISBN: {isbn}")
            return
        
        disponible = input("¿Disponible? (s/n): ").lower() == "s"
        cls(titulo, autor, isbn, disponible)
        print("✅ Libro agregado correctamente.")

    def prestar(self):
        if self.disponible:
            self.disponible = False
            print(f'📚 "{self.titulo}" ha sido prestado.')
        else:
            print(f'❌ "{self.titulo}" ya está prestado.')
        Libro.guardar_datos()  # Guardar cambios

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            print(f'📦 "{self.titulo}" ha sido devuelto.')
        else:
            print(f'✅ "{self.titulo}" ya estaba disponible.')
        Libro.guardar_datos()  # Guardar cambios

    @classmethod
    def mostrar(cls):
        if not cls.libros:
            print("⚠️ No hay libros registrados.")
            return
        
        print("\n📚 Biblioteca Completa:")
        for libro in cls.libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            print(f'• "{libro.titulo}" - {libro.autor} (ISBN: {libro.isbn}) - {estado}')

    @classmethod
    def buscar(cls, isbn: str = None):
        if not isbn:
            isbn = input("Ingrese el ISBN a buscar: ").strip()
        
        for libro in cls.libros:
            if libro.isbn == isbn:
                return libro
        
        print(f"\n❌ No se encontró el ISBN: {isbn}")
        return None

def main():
    Libro.cargar_datos()  # Cargar datos al iniciar

    while True:
        print("\n--- Menú de Biblioteca ---")
        print("a) Agregar libro")
        print("b) Prestar libro")
        print("c) Devolver libro")
        print("d) Mostrar todos los libros")
        print("e) Salir")
        
        opcion = input("Seleccione una opción: ").strip().lower()
        
        if opcion == 'a':
            print("\n--- Agregar Nuevo Libro ---")
            Libro.agregar()
            
        elif opcion == 'b':
            print("\n--- Prestar Libro ---")
            isbn = input("ISBN del libro a prestar: ").strip()
            libro = Libro.buscar(isbn)
            if libro:
                libro.prestar()
                
        elif opcion == 'c':
            print("\n--- Devolver Libro ---")
            isbn = input("ISBN del libro a devolver: ").strip()
            libro = Libro.buscar(isbn)
            if libro:
                libro.devolver()
                
        elif opcion == 'd':
            Libro.mostrar()
            
        elif opcion == 'e':
            print("\n¡Hasta luego! 📖")
            break
            
        else:
            print("⚠️ Opción inválida. Por favor, seleccione una opción del menú.")

if __name__ == "__main__":
    main()