import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar
from modulos.modulo_clientes import ModuloClientes
from modulos.modulo_vehiculos import ModuloVehiculos
from modulos.modulo_dispositivos import ModuloDispositivos
from modulos.modulo_informes import ModuloInformes
from tema import aplicar_tema, alternar_tema

def abrir_clientes():
    ventana_clientes = tk.Toplevel(root)
    ModuloClientes(ventana_clientes)
def abrir_vehiculos():
    ventana_vehiculos = tk.Toplevel(root)
    ModuloVehiculos(ventana_vehiculos)
def abrir_dispositivos():
    ventana_dispositivos = tk.Toplevel(root)
    ModuloDispositivos(ventana_dispositivos)
def abrir_informes():
    ventana_informes = tk.Toplevel(root)
    ModuloInformes(ventana_informes)
def salir():
    if messagebox.askyesno("Salir", "Desea salir del sistema?"):
        root.destroy()
def cambiar_tema():
    alternar_tema()
    aplicar_tema(root, estilo)

# Ventana principal
root = tk.Tk()
root.title("SecureSys")
root.geometry("500x580")
root.resizable(False, False)

# =========================
# ESTILO TTK
# =========================
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "Menu.TButton",
    font=("Segoe UI Emoji", 11),
    padding=10
)
estilo.configure(
    "Salir.TButton",
    font=("Segoe UI Emoji", 11, "bold"),
    padding=10
)

# Titulo
titulo = tk.Label(
    root,
    text="SecureSys",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=30)
subtitulo = tk.Label(
    root,
    text="Sistema de gestion de servicios de seguridad",
    font=("Arial", 11)
)
subtitulo.pack(pady=5)

# =========================
# Botones
# =========================

ttk.Button(
    root,
    text="👥 Clientes",
    width=25,
    style="Menu.TButton",
    command=abrir_clientes
).pack(pady=8)

ttk.Button(
    root,
    text="🚓 Vehiculos",
    width=25,
    style="Menu.TButton",
    command=abrir_vehiculos
).pack(pady=8)
ttk.Button(
    root,
    text="📡 Dispositivos",
    width=25,
    style="Menu.TButton",
    command=abrir_dispositivos
).pack(pady=8)
ttk.Button(
    root,
    text="🗂 Informes",
    width=25,
    style="Menu.TButton",
    command=abrir_informes
).pack(pady=8)
ttk.Button(
    root,
    text="🚪 Salir",
    width=25,
    style="Salir.TButton",
    command=salir
).pack(pady=15)
ttk.Button(
    root,
    text="🌓 Cambiar Tema",
    width=25,
    style="Menu.TButton",
    command=cambiar_tema
).pack(pady=5)

# Aplicar el tema guardado (se mantiene al abrir cualquier modulo)
aplicar_tema(root, estilo)

root.mainloop()
