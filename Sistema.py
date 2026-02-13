import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import hashlib


#Base de datos Con SQL y Creacion de estas tablas
conexion = sqlite3.connect("finanzas.db")
cursor = conexion.cursor()

def crear_tablas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        documento TEXT UNIQUE NOT NULL,
        contraseña TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tipo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)
    conexion.commit()

crear_tablas()



def encriptar(password):
    return hashlib.sha256(password.encode()).hexdigest()



def registrar_usuario(documento, contraseña):
    try:
        cursor.execute(
            "INSERT INTO usuarios (documento, contraseña) VALUES (?, ?)",
            (documento, encriptar(contraseña))
        )
        conexion.commit()
        return True
    except:
        return False


def verificar_login(documento, contraseña):
    cursor.execute(
        "SELECT id FROM usuarios WHERE documento=? AND contraseña=?",
        (documento, encriptar(contraseña))
    )
    return cursor.fetchone()



def guardar_movimiento(tipo, descripcion, monto):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor.execute(
        "INSERT INTO movimientos (usuario_id, tipo, descripcion, monto, fecha) VALUES (?, ?, ?, ?, ?)",
        (usuario_actual, tipo, descripcion, monto, fecha)
    )
    conexion.commit()

def obtener_saldo():
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN tipo='ingreso' THEN monto END), 0) -
            COALESCE(SUM(CASE WHEN tipo='egreso' THEN monto END), 0)
        FROM movimientos
        WHERE usuario_id=?
    """, (usuario_actual,))
    return cursor.fetchone()[0]

def obtener_historial():
    cursor.execute("""
        SELECT tipo, descripcion, monto, fecha
        FROM movimientos
        WHERE usuario_id=?
        ORDER BY id DESC
    """, (usuario_actual,))
    return cursor.fetchall()



def iniciar_sistema():
# Estilo
    ventana = tk.Tk()
    ventana.title("Sistema Financiero PRO")
    ventana.geometry("900x650")
    ventana.configure(bg="#17233F")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
        background="#1E293B",
        foreground="white",
        rowheight=28,
        fieldbackground="#1E293B"
    )

    style.map("Treeview", background=[("selected", "#334155")])


#FUNCIONES
    def limpiar_campos():
        entry_descripcion.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

    def actualizar_saldo():
        saldo = obtener_saldo()
        label_saldo.config(text=f"Saldo actual: ${saldo:,.2f}")

    def cargar_historial():
        tabla.delete(*tabla.get_children())
        for tipo, desc, monto, fecha in obtener_historial():
            tabla.insert("", tk.END, values=(tipo, desc, f"${monto:,.2f}", fecha))

    def agregar_ingreso():
        try:
            descripcion = entry_descripcion.get().strip()
            monto = float(entry_monto.get())

            if not descripcion:
                messagebox.showerror("Error", "Ingrese una descripción")
                return

            guardar_movimiento("ingreso", descripcion, monto)
            limpiar_campos()
            actualizar_saldo()
            cargar_historial()

        except ValueError:
            messagebox.showerror("Error", "Monto inválido")

    def agregar_egreso():
        try:
            descripcion = entry_descripcion.get().strip()
            monto = float(entry_monto.get())

            if not descripcion:
                messagebox.showerror("Error", "Ingrese una descripción")
                return

            guardar_movimiento("egreso", descripcion, monto)
            limpiar_campos()
            actualizar_saldo()
            cargar_historial()

        except ValueError:
            messagebox.showerror("Error", "Monto inválido")



    barra = tk.Frame(ventana, bg="#111827", height=60)
    barra.pack(fill="x")
    tk

    tk.Label(
        barra,
        text="💰 Sistema Financiero",
        bg="#111827",
        fg="white",
        font=("Segoe UI", 16, "bold")
    ).pack(side="left", padx=20)
#Bu
    tk.Button(
        barra,
        text="Cerrar sesión",
        bg="#DC2626",
        fg="white",
        relief="flat",
        command=lambda: [ventana.destroy(), ventana_login()]
    ).pack(side="right", padx=20)



    frame_form = tk.Frame(ventana, bg="#1E293B")
    frame_form.pack(pady=20, padx=40, fill="x")

    tk.Label(
        frame_form,
        text="Registrar Movimiento",
        bg="#1E293B",
        fg="white",
        font=("Segoe UI", 14, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_form, text="Descripción", bg="#1E293B", fg="#CBD5E1").grid(row=1, column=0, sticky="w", pady=5)
    entry_descripcion = tk.Entry(frame_form, width=40, bg="#334155", fg="white", insertbackground="white")
    entry_descripcion.grid(row=1, column=1, pady=5)

    tk.Label(frame_form, text="Monto", bg="#1E293B", fg="#CBD5E1").grid(row=2, column=0, sticky="w", pady=5)
    entry_monto = tk.Entry(frame_form, width=40, bg="#334155", fg="white", insertbackground="white")
    entry_monto.grid(row=2, column=1, pady=5)

    tk.Button(frame_form, text="AGREGAR DINERO", bg="#16A34A",
              fg="white", width=18, relief="flat",
              command=agregar_ingreso).grid(row=3, column=0, pady=15)

    tk.Button(frame_form, text="RETIRAR", bg="#DC2626",
              fg="white", width=18, relief="flat",
              command=agregar_egreso).grid(row=3, column=1, pady=15)



    frame_saldo = tk.Frame(ventana, bg="#1E293B")
    frame_saldo.pack(pady=10, padx=40, fill="x")

    label_saldo = tk.Label(
        frame_saldo,
        text="Saldo actual: $0.00",
        font=("Segoe UI", 18, "bold"),
        bg="#1E293B",
        fg="#FACC15"
    )
    label_saldo.pack(pady=15)



    tabla_frame = tk.Frame(ventana, bg="#0F172A")
    tabla_frame.pack(padx=40, pady=20, fill="both", expand=True)

    columns = ("Tipo", "Descripción", "Monto", "Fecha")
    tabla = ttk.Treeview(tabla_frame, columns=columns, show="headings")

    for col in columns:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    tabla.pack(fill="both", expand=True)

    actualizar_saldo()
    cargar_historial()

    ventana.mainloop()



def ventana_login():

    login = tk.Tk()
    login.title("Login")
    login.geometry("350x350")
    login.configure(bg="#0F172A")

    tk.Label(login, text="Iniciar Sesión",
             bg="#0F172A", fg="white",
             font=("Segoe UI", 16, "bold")).pack(pady=20)

    tk.Label(login, text="Documento", bg="#0F172A", fg="white").pack()
    entry_doc = tk.Entry(login)
    entry_doc.pack(pady=5)

    tk.Label(login, text="Contraseña", bg="#0F172A", fg="white").pack()
    entry_pass = tk.Entry(login, show="*")
    entry_pass.pack(pady=5)

    def iniciar_sesion():
        doc = entry_doc.get()
        pas = entry_pass.get()
        usuario = verificar_login(doc, pas)

        if usuario:
            global usuario_actual
            usuario_actual = usuario[0]
            login.destroy()
            iniciar_sistema()
        else:
            messagebox.showerror("Error", "Datos incorrectos")

    def registrar():
        doc = entry_doc.get()
        pas = entry_pass.get()

        if registrar_usuario(doc, pas):
            messagebox.showinfo("Éxito", "Usuario registrado")
        else:
            messagebox.showerror("Error", "Usuario ya existe")

    tk.Button(login, text="Iniciar sesión",
              bg="#16A34A", fg="white",
              command=iniciar_sesion).pack(pady=10)

    tk.Button(login, text="Registrarse",
              bg="#2563EB", fg="white",
              command=registrar).pack()

    login.mainloop()


ventana_login()
conexion.close()
