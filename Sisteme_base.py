import sqlite3
import tkinter as tk
import hashlib
from tkinter import ttk, messagebox



conexion = sqlite3.connect("finanzas.db")
cursor = conexion.cursor()



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


def administrar_usuarios():
    ventana_admin = tk.Toplevel()
    ventana_admin.title("Administrar Usuarios")
    ventana_admin.geometry("700x450")
    ventana_admin.configure(bg="#0F172A")

    tk.Label(
        ventana_admin,
        text="Administrar Usuarios",
        bg="#0F172A",
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=10)

    frame_tabla = tk.Frame(ventana_admin, bg="#0F172A")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("ID", "Documento", "Nombre", "Apellido")
    tabla_admin = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla_admin.heading(col, text=col)
        tabla_admin.column(col, anchor="center")

    tabla_admin.pack(fill="both", expand=True)



    def cargar_usuarios():
        tabla_admin.delete(*tabla_admin.get_children())
        cursor.execute("SELECT id, documento, nombre, apellido FROM usuarios")
        for fila in cursor.fetchall():
            tabla_admin.insert("", "end", values=fila)

    cargar_usuarios()

    def eliminar_usuario():
        selection = tabla_admin.selection()
        if not selection:
            messagebox.showwarning("Atención", "Seleccione un usuario para eliminar")
            return

        usuario = tabla_admin.item(selection[0])["values"]
        id_usuario = usuario[0]

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar usuario {usuario[1]}?")
        if confirm:
            cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
            conexion.commit()
            cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario eliminado")

    def editar_usuario():
        selection = tabla_admin.selection()
        if not selection:
            messagebox.showwarning("Atención", "Seleccione un usuario para editar")
            return

        usuario = tabla_admin.item(selection[0])["values"]
        id_usuario = usuario[0]

        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Usuario")
        ventana_editar.geometry("350x300")
        ventana_editar.configure(bg="#0F172A")

        tk.Label(ventana_editar, text="Documento", bg="#0F172A", fg="white").pack(pady=5)
        entry_doc_ed = tk.Entry(ventana_editar)
        entry_doc_ed.insert(0, usuario[1])
        entry_doc_ed.pack()

        tk.Label(ventana_editar, text="Nombre", bg="#0F172A", fg="white").pack(pady=5)
        entry_nombre_ed = tk.Entry(ventana_editar)
        entry_nombre_ed.insert(0, usuario[2])
        entry_nombre_ed.pack()

        tk.Label(ventana_editar, text="Apellido", bg="#0F172A", fg="white").pack(pady=5)
        entry_apellido_ed = tk.Entry(ventana_editar)
        entry_apellido_ed.insert(0, usuario[3])
        entry_apellido_ed.pack()

        def guardar_cambios():
            nuevo_doc = entry_doc_ed.get().strip()
            nuevo_nom = entry_nombre_ed.get().strip()
            nuevo_ape = entry_apellido_ed.get().strip()

            if not nuevo_doc or not nuevo_nom or not nuevo_ape:
                messagebox.showerror("Error", "Complete todos los campos")
                return

            cursor.execute("""
                UPDATE usuarios
                SET documento=?, nombre=?, apellido=?
                WHERE id=?
            """, (nuevo_doc, nuevo_nom, nuevo_ape, id_usuario))
            conexion.commit()

            ventana_editar.destroy()
            cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario actualizado")

        tk.Button(ventana_editar, text="Guardar cambios",
                  bg="#16A34A", fg="white",
                  command=guardar_cambios).pack(pady=10)

    def agregar_usuario_admin():
        ventana_agregar = tk.Toplevel()
        ventana_agregar.title("Agregar usuario")
        ventana_agregar.geometry("350x330")
        ventana_agregar.configure(bg="#0F172A")

        tk.Label(ventana_agregar, text="Documento", bg="#0F172A", fg="white").pack(pady=5)
        entry_doc_ag = tk.Entry(ventana_agregar)
        entry_doc_ag.pack()

        tk.Label(ventana_agregar, text="Nombre", bg="#0F172A", fg="white").pack(pady=5)
        entry_nombre_ag = tk.Entry(ventana_agregar)
        entry_nombre_ag.pack()

        tk.Label(ventana_agregar, text="Apellido", bg="#0F172A", fg="white").pack(pady=5)
        entry_apellido_ag = tk.Entry(ventana_agregar)
        entry_apellido_ag.pack()

        tk.Label(ventana_agregar, text="Contraseña", bg="#0F172A", fg="white").pack(pady=5)
        entry_pass_ag = tk.Entry(ventana_agregar, show="*")
        entry_pass_ag.pack()

        def guardar_agregado():
            doc = entry_doc_ag.get().strip()
            nom = entry_nombre_ag.get().strip()
            ape = entry_apellido_ag.get().strip()
            pas = entry_pass_ag.get().strip()

            if not doc or not nom or not ape or not pas:
                messagebox.showerror("Error", "Complete todos los campos")
                return

            try:
                cursor.execute(
                    "INSERT INTO usuarios (documento, nombre, apellido, contraseña) VALUES (?, ?, ?, ?)",
                    (doc, nom, ape, hashlib.sha256(pas.encode()).hexdigest())
                )
                conexion.commit()
                cargar_usuarios()
                ventana_agregar.destroy()
                messagebox.showinfo("Éxito", "Usuario agregado")
            except:
                messagebox.showerror("Error", "No se pudo agregar el usuario")

        tk.Button(ventana_agregar, text="Agregar usuario",
                  bg="#2563EB", fg="white",
                  command=guardar_agregado).pack(pady=10)



    botones_frame = tk.Frame(ventana_admin, bg="#0F172A")
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Eliminar usuario",
              bg="#DC2626", fg="white", command=eliminar_usuario).grid(row=0, column=0, padx=10)

    tk.Button(botones_frame, text="Editar usuario",
              bg="#2563EB", fg="white", command=editar_usuario).grid(row=0, column=1, padx=10)

    tk.Button(botones_frame, text="Agregar usuario",
              bg="#16A34A", fg="white", command=agregar_usuario_admin).grid(row=0, column=2, padx=10)



root = tk.Tk()
root.title("Sistema de Usuarios")
root.geometry("300x200")
root.configure(bg="#0F172A")

tk.Button(
    root,
    text="Ver Usuarios",
    bg="#2563EB",
    fg="white",
    command=ver_base_de_datos
).pack(pady=10)

tk.Button(
    root,
    text="Administrar Usuarios",
    bg="#16A34A",
    fg="white",
    command=administrar_usuarios
).pack(pady=10)

root.mainloop()

conexion.close()