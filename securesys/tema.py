import json
import os
import tkinter as tk


ARCHIVO_CONFIG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tema_config.json"
)

TEMAS = {
    "claro": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "boton_bg": "#e1e1e1",
        "boton_fg": "#000000",
        "tabla_bg": "#ffffff",
        "tabla_fg": "#000000",
        "tabla_encabezado_bg": "#d9d9d9",
        "seleccion_bg": "#0078d7",
        "seleccion_fg": "#ffffff"
    },
    "oscuro": {
        "bg": "#2b2b2b",
        "fg": "#ffffff",
        "entry_bg": "#3c3f41",
        "entry_fg": "#ffffff",
        "boton_bg": "#3c3f41",
        "boton_fg": "#ffffff",
        "tabla_bg": "#313335",
        "tabla_fg": "#ffffff",
        "tabla_encabezado_bg": "#3c3f41",
        "seleccion_bg": "#4a6f9e",
        "seleccion_fg": "#ffffff"
    }
}


def _cargar_tema_guardado():

    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            nombre = datos.get("tema", "claro")

            if nombre in TEMAS:
                return nombre

    except Exception:
        pass

    return "claro"


def _guardar_tema(nombre_tema):

    try:
        with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as archivo:
            json.dump({"tema": nombre_tema}, archivo)

    except Exception:
        pass


# Tema activo compartido por toda la aplicacion (persiste en disco)
tema_actual = _cargar_tema_guardado()


def obtener_tema_actual():
    return tema_actual


def alternar_tema():

    global tema_actual

    tema_actual = "oscuro" if tema_actual == "claro" else "claro"
    _guardar_tema(tema_actual)

    return tema_actual


def establecer_tema(nombre_tema):

    global tema_actual

    if nombre_tema in TEMAS:
        tema_actual = nombre_tema
        _guardar_tema(tema_actual)


def _colorear_widget(widget, colores, excluir):

    if widget in excluir:
        return

    clase = widget.winfo_class()

    try:
        if clase in ("Frame", "Labelframe", "Toplevel", "Tk"):
            widget.configure(bg=colores["bg"])

        elif clase == "Label":
            widget.configure(
                bg=colores["bg"],
                fg=colores["fg"]
            )

        elif clase == "Entry":
            widget.configure(
                bg=colores["entry_bg"],
                fg=colores["entry_fg"],
                insertbackground=colores["entry_fg"]
            )

        elif clase == "Button":
            widget.configure(
                bg=colores["boton_bg"],
                fg=colores["boton_fg"],
                activebackground=colores["seleccion_bg"],
                activeforeground=colores["seleccion_fg"]
            )

    except tk.TclError:
        pass

    for hijo in widget.winfo_children():
        _colorear_widget(hijo, colores, excluir)


def aplicar_tema(ventana, estilo_ttk, nombre_tema=None, excluir_widgets=None):
    """
    Aplica el tema claro/oscuro a los widgets clasicos de tkinter
    (Label, Entry, Frame, Button) y a los widgets ttk (Button,
    Combobox, Treeview) de la ventana indicada.

    excluir_widgets: lista opcional de widgets que no deben
    recolorearse (por ejemplo, el recuadro de vista previa de
    una imagen, que debe mantenerse siempre claro).
    """

    global tema_actual

    if nombre_tema is None:
        nombre_tema = tema_actual
    else:
        tema_actual = nombre_tema

    colores = TEMAS[tema_actual]
    excluir = set(excluir_widgets or [])

    ventana.configure(bg=colores["bg"])

    _colorear_widget(ventana, colores, excluir)

    estilo_ttk.theme_use("clam")

    estilo_ttk.configure(
        "TButton",
        background=colores["boton_bg"],
        foreground=colores["boton_fg"]
    )

    estilo_ttk.map(
        "TButton",
        background=[("active", colores["seleccion_bg"])],
        foreground=[("active", colores["seleccion_fg"])]
    )

    estilo_ttk.configure(
        "Icono.TButton",
        background=colores["boton_bg"],
        foreground=colores["boton_fg"]
    )

    estilo_ttk.map(
        "Icono.TButton",
        background=[("active", colores["seleccion_bg"])],
        foreground=[("active", colores["seleccion_fg"])]
    )

    estilo_ttk.configure(
        "Menu.TButton",
        background=colores["boton_bg"],
        foreground=colores["boton_fg"]
    )

    estilo_ttk.map(
        "Menu.TButton",
        background=[("active", colores["seleccion_bg"])],
        foreground=[("active", colores["seleccion_fg"])]
    )

    estilo_ttk.configure(
        "Salir.TButton",
        background=colores["boton_bg"],
        foreground=colores["boton_fg"]
    )

    estilo_ttk.map(
        "Salir.TButton",
        background=[("active", colores["seleccion_bg"])],
        foreground=[("active", colores["seleccion_fg"])]
    )

    estilo_ttk.configure(
        "TCombobox",
        fieldbackground=colores["entry_bg"],
        background=colores["boton_bg"],
        foreground=colores["entry_fg"]
    )

    estilo_ttk.configure(
        "TEntry",
        fieldbackground=colores["entry_bg"],
        foreground=colores["entry_fg"]
    )

    estilo_ttk.configure(
        "Treeview",
        background=colores["tabla_bg"],
        fieldbackground=colores["tabla_bg"],
        foreground=colores["tabla_fg"]
    )

    estilo_ttk.configure(
        "Treeview.Heading",
        background=colores["tabla_encabezado_bg"],
        foreground=colores["fg"]
    )

    estilo_ttk.map(
        "Treeview",
        background=[("selected", colores["seleccion_bg"])],
        foreground=[("selected", colores["seleccion_fg"])]
    )
