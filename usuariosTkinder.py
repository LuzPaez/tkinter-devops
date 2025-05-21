import sqlite3
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos
def conectar_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT,
            edad INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Función para agregar un usuario
def agregar_usuario():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    telefono = entry_telefono.get()
    direccion = entry_direccion.get()
    edad = entry_edad.get()
    
    if nombre and apellido and email:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, apellido, email, telefono, direccion, edad) VALUES (?, ?, ?, ?, ?, ?)", 
                       (nombre, apellido, email, telefono, direccion, edad))
        conn.commit()
        conn.close()
        limpiar_campos()
        mostrar_usuarios()
    else:
        messagebox.showwarning("Error", "Nombre, Apellido y Email son obligatorios")

# Función para mostrar los usuarios
def mostrar_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    listbox_usuarios.delete(0, tk.END)
    for usuario in usuarios:
        listbox_usuarios.insert(tk.END, usuario)

# Función para buscar usuario por ID
def buscar_usuario():
    usuario_id = entry_id.get()
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        listbox_usuarios.delete(0, tk.END)
        listbox_usuarios.insert(tk.END, usuario)
    else:
        messagebox.showinfo("Resultado", "Usuario no encontrado")

# Función para actualizar usuario
def actualizar_usuario():
    usuario_id = entry_id.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    telefono = entry_telefono.get()
    direccion = entry_direccion.get()
    edad = entry_edad.get()
    
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios SET nombre=?, apellido=?, email=?, telefono=?, direccion=?, edad=? WHERE id=?
    """, (nombre, apellido, email, telefono, direccion, edad, usuario_id))
    conn.commit()
    conn.close()
    limpiar_campos()
    mostrar_usuarios()

# Función para eliminar un usuario
def eliminar_usuario():
    usuario_id = entry_id.get()
    if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este usuario?"):
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()
        mostrar_usuarios()

# Función para limpiar campos
def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_edad.delete(0, tk.END)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("CRUD Usuarios")
root.configure(bg="#d0e1f9")

conectar_db()

frame_form = tk.Frame(root, bg="#d0e1f9")
frame_form.grid(row=0, column=0, padx=10, pady=10)

frame_buttons = tk.Frame(root, bg="#d0e1f9")
frame_buttons.grid(row=1, column=0, pady=10)

frame_list = tk.Frame(root, bg="#d0e1f9")
frame_list.grid(row=2, column=0, pady=10)

# Campos de entrada
tk.Label(frame_form, text="ID:", bg="#d0e1f9").grid(row=0, column=0)
entry_id = tk.Entry(frame_form)
entry_id.grid(row=0, column=1)

tk.Label(frame_form, text="Nombre:", bg="#d0e1f9").grid(row=1, column=0)
entry_nombre = tk.Entry(frame_form)
entry_nombre.grid(row=1, column=1)

tk.Label(frame_form, text="Apellido:", bg="#d0e1f9").grid(row=2, column=0)
entry_apellido = tk.Entry(frame_form)
entry_apellido.grid(row=2, column=1)

tk.Label(frame_form, text="Email:", bg="#d0e1f9").grid(row=3, column=0)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=3, column=1)

tk.Label(frame_form, text="Teléfono:", bg="#d0e1f9").grid(row=4, column=0)
entry_telefono = tk.Entry(frame_form)
entry_telefono.grid(row=4, column=1)

tk.Label(frame_form, text="Dirección:", bg="#d0e1f9").grid(row=5, column=0)
entry_direccion = tk.Entry(frame_form)
entry_direccion.grid(row=5, column=1)

tk.Label(frame_form, text="Edad:", bg="#d0e1f9").grid(row=6, column=0)
entry_edad = tk.Entry(frame_form)
entry_edad.grid(row=6, column=1)

# Botones organizados
tk.Button(frame_buttons, text="Agregar", command=agregar_usuario, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Buscar", command=buscar_usuario, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Actualizar", command=actualizar_usuario, bg="#FFC107", fg="black").grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Eliminar", command=eliminar_usuario, bg="#F44336", fg="white").grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="Limpiar", command=limpiar_campos, bg="#9E9E9E", fg="white").grid(row=0, column=4, padx=5)
tk.Button(frame_buttons, text="Ver Todos", command=mostrar_usuarios, bg="#673AB7", fg="white").grid(row=0, column=5, padx=5)

listbox_usuarios = tk.Listbox(frame_list, width=80)
listbox_usuarios.pack()

mostrar_usuarios()
root.mainloop()
