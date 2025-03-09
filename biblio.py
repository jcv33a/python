class Libro:
    libros = []  # Lista para almacenar todas las instancias

    def __init__(self, titulo: str, autor: str, isbn: str, disponible: bool = True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible
        Libro.libros.append(self)

    @classmethod
    def agregar(cls):
        titulo = input("Ingrese el título: ")
        autor = input("Ingrese el autor: ")
        isbn = input("Ingrese el ISBN: ")
        disponible = input("¿Disponible? (s/n): ").lower() == "s"
        return cls(titulo, autor, isbn, disponible)

    def prestar(self):
        if self.disponible:
            self.disponible = False
            print(f'📚 "{self.titulo}" ha sido prestado.')
        else:
            print(f'❌ "{self.titulo}" ya está prestado.')

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            print(f'📦 "{self.titulo}" ha sido devuelto.')
        else:
            print(f'✅ "{self.titulo}" ya estaba disponible.')

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
            print("✅ Libro agregado correctamente.")
            
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