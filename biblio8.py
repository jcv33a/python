import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

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
    def agregar(cls, titulo, autor, isbn, disponible):
        """Agrega un libro con validación de ISBN único"""
        if cls.buscar(isbn):
            messagebox.showerror("Error", f"❌ Ya existe un libro con el ISBN: {isbn}")
            return

        cls(titulo, autor, isbn, disponible)
        messagebox.showinfo("Éxito", "✅ Libro agregado correctamente.")

    def prestar(self):
        if self.disponible:
            self.disponible = False
            messagebox.showinfo("Éxito", f'📚 "{self.titulo}" ha sido prestado.')
        else:
            messagebox.showerror("Error", f'❌ "{self.titulo}" ya está prestado.')
        Libro.guardar_datos()  # Guardar cambios

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            messagebox.showinfo("Éxito", f'📦 "{self.titulo}" ha sido devuelto.')
        else:
            messagebox.showinfo("Info", f'✅ "{self.titulo}" ya estaba disponible.')
        Libro.guardar_datos()  # Guardar cambios

    @classmethod
    def mostrar(cls):
        if not cls.libros:
            messagebox.showinfo("Info", "⚠️ No hay libros registrados.")
            return

        libros_str = "\n📚 Biblioteca Completa:\n"
        for libro in cls.libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            libros_str += f'• "{libro.titulo}" - {libro.autor} (ISBN: {libro.isbn}) - {estado}\n'
        messagebox.showinfo("Biblioteca", libros_str)

    @classmethod
    def buscar(cls, isbn: str = None):
        for libro in cls.libros:
            if libro.isbn == isbn:
                return libro
        return None

    @classmethod
    def eliminar(cls, isbn):
        """Elimina un libro dado un ISBN"""
        libro = cls.buscar(isbn)
        if libro:
            cls.libros.remove(libro)
            cls.guardar_datos()
            messagebox.showinfo("Éxito", f"✅ Libro con ISBN {isbn} ha sido eliminado correctamente.")
        else:
            messagebox.showerror("Error", f"❌ No se encontró un libro con el ISBN: {isbn}")

def agregar_libro():
    titulo = simpledialog.askstring("Agregar Libro", "Ingrese el título:")
    autor = simpledialog.askstring("Agregar Libro", "Ingrese el autor:")
    isbn = simpledialog.askstring("Agregar Libro", "Ingrese el ISBN:")
    disponible = messagebox.askyesno("Agregar Libro", "¿Disponible?")
    if titulo and autor and isbn:
        Libro.agregar(titulo, autor, isbn, disponible)

def prestar_libro():
    isbn = simpledialog.askstring("Prestar Libro", "Ingrese el ISBN del libro a prestar:")
    libro = Libro.buscar(isbn)
    if libro:
        libro.prestar()
    else:
        messagebox.showerror("Error", f"❌ No se encontró el ISBN: {isbn}")

def devolver_libro():
    isbn = simpledialog.askstring("Devolver Libro", "Ingrese el ISBN del libro a devolver:")
    libro = Libro.buscar(isbn)
    if libro:
        libro.devolver()
    else:
        messagebox.showerror("Error", f"❌ No se encontró el ISBN: {isbn}")

def mostrar_libros():
    Libro.mostrar()

def eliminar_libro():
    isbn = simpledialog.askstring("Eliminar Libro", "Ingrese el ISBN del libro a eliminar:")
    if isbn:
        Libro.eliminar(isbn)

def main():
    Libro.cargar_datos()  # Cargar datos al iniciar

    root = tk.Tk()
    root.title("Biblioteca")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    menu_frame = ttk.Frame(frame, padding="10", relief="raised", width=100, height=100)
    menu_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
    menu_frame.grid_propagate(False)  # Prevent the frame from resizing to fit its content

    ttk.Button(menu_frame, text="Agregar Libro", command=agregar_libro).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(menu_frame, text="Prestar Libro", command=prestar_libro).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(menu_frame, text="Devolver Libro", command=devolver_libro).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(menu_frame, text="Mostrar Libros", command=mostrar_libros).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(menu_frame, text="Eliminar Libro", command=eliminar_libro).grid(row=0, column=4, padx=5, pady=5)
    ttk.Button(menu_frame, text="Salir", command=root.destroy).grid(row=0, column=5, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()