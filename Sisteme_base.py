import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Conexión a la base de datos ----------------

conexion = sqlite3.connect("finanzas.db")
cursor = conexion.cursor()

# ---------------- Función para visualizar usuarios ----------------

def ver_base_de_datos():
    ventana_bd = tk.Toplevel()
    ventana_bd.title("Usuarios Registrados en la Base de Datos")
    ventana_bd.geometry("600x400")
    ventana_bd.configure(bg="#0F172A")

    tk.Label(
        ventana_bd,
        text="Usuarios en la Base de Datos",
        bg="#0F172A",
        fg="white",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=10)

    frame_tabla = tk.Frame(ventana_bd, bg="#0F172A")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("ID", "Documento", "Nombre", "Apellido", "Contraseña")
    tabla_bd = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla_bd.heading(col, text=col)
        tabla_bd.column(col, anchor="center")

    tabla_bd.pack(fill="both", expand=True)

    try:
        cursor.execute("SELECT id, documento, nombre, apellido, contraseña FROM usuarios")
        registros = cursor.fetchall()

        for fila in registros:
            tabla_bd.insert("", "end", values=fila)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{e}")

    tk.Button(
        ventana_bd,
        text="Cerrar",
        bg="#DC2626",
        fg="white",
        command=ventana_bd.destroy
    ).pack(pady=10)

# ---------------- Mostrar ventana principal mínima ----------------

root = tk.Tk()
root.title("Visualizar Usuarios")
root.geometry("300x200")
root.configure(bg="#0F172A")

tk.Button(
    root,
    text="Ver Usuarios",
    bg="#2563EB",
    fg="white",
    command=ver_base_de_datos
).pack(expand=True, pady=50)

root.mainloop()

conexion.close()