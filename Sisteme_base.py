import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def ver_usuarios():

    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Usuarios Registrados")
    ventana_usuarios.geometry("600x400")
    ventana_usuarios.configure(bg="#0F172A")

    tk.Label(
        ventana_usuarios,
        text="Usuarios Registrados",
        bg="#0F172A",
        fg="white",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=15)

    # Frame tabla
    frame_tabla = tk.Frame(ventana_usuarios, bg="#0F172A")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("ID", "Documento", "Contraseña")

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    tabla.pack(fill="both", expand=True)

    # Cargar datos desde la base de datos
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, documento, contrasena FROM usuarios")
        usuarios = cursor.fetchall()

        for usuario in usuarios:
            tabla.insert("", "end", values=usuario)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios\n{e}")