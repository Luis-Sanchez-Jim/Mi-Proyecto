import os
import shutil

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from PIL import Image, ImageTk, ImageFilter

from conexion import conectar
from exportar import exportar_excel, exportar_pdf
from tema import aplicar_tema, alternar_tema


# =========================
# CONFIGURACION DE IMAGENES
# =========================
EXTENSIONES_PERMITIDAS = (".jpg", ".jpeg", ".png")
TAMANO_MAXIMO_MB = 5
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024
CARPETA_IMAGENES = "imagenes_clientes"
DIMENSION_MAXIMA = 800
DIMENSION_MINIATURA = (150, 150)

os.makedirs(CARPETA_IMAGENES, exist_ok=True)


class ModuloClientes:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("SecureSys - Clientes")
        self.ventana.geometry("900x680")

        estilo = ttk.Style()
        estilo.configure(
            "Icono.TButton",
            font=("Segoe UI Emoji", 10),
            padding=6
        )
        self.estilo = estilo

# =========================
# TITULO
# =========================
        tk.Label(
            ventana,
            text="Gestion de Clientes",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

# =========================
# FORMULARIO
# =========================
        formulario = tk.Frame(ventana)
        formulario.pack(pady=5)

        tk.Label(formulario, text="Codigo:").grid(
            row=0, column=0, padx=10, pady=5
        )

        self.codigo = tk.Entry(formulario, width=30)
        self.codigo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Nombre:").grid(
            row=1, column=0, padx=10, pady=5
        )

        self.nombre = tk.Entry(formulario, width=30)
        self.nombre.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Telefono:").grid(
            row=2, column=0, padx=10, pady=5
        )

        self.telefono = tk.Entry(formulario, width=30)
        self.telefono.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Tipo:").grid(
            row=3, column=0, padx=10, pady=5
        )

        self.tipo = ttk.Combobox(
            formulario,
            values=[
                "Residencial",
                "Comercial",
                "Industrial",
                "Gubernamental"
            ],
            state="readonly",
            width=27
        )
        self.tipo.grid(row=3, column=1, padx=10, pady=5)

# Foto
        tk.Label(formulario, text="Foto:").grid(
            row=4, column=0, padx=10, pady=5
        )

        foto_frame = tk.Frame(formulario)
        foto_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.label_imagen = tk.Label(
            foto_frame,
            text="Sin imagen",
            width=18,
            height=8,
            relief="groove",
            bg="white"
        )
        self.label_imagen.pack(side="left", padx=(0, 10))

        botones_foto = tk.Frame(foto_frame)
        botones_foto.pack(side="left")

        ttk.Button(
            botones_foto,
            text="🖼 Seleccionar Imagen",
            style="Icono.TButton",
            command=self.seleccionar_imagen
        ).pack(pady=2, fill="x")

        ttk.Button(
            botones_foto,
            text="⬇ Descargar Imagen",
            style="Icono.TButton",
            command=self.descargar_imagen
        ).pack(pady=2, fill="x")

        ttk.Button(
            botones_foto,
            text="❌ Quitar Imagen",
            style="Icono.TButton",
            command=self.quitar_imagen
        ).pack(pady=2, fill="x")

        self.ruta_imagen_nueva = None
        self.nombre_imagen_actual = None
        self.imagen_tk = None
        self.fotos_cache = {}

# =========================
# BUSQUEDA
# =========================
        busqueda = tk.Frame(ventana)
        busqueda.pack(pady=10)

        tk.Label(
            busqueda,
            text="Buscar:"
        ).pack(side="left", padx=5)

        self.buscar = tk.Entry(
            busqueda,
            width=30
        )
        self.buscar.pack(side="left", padx=5)

# =========================
# BOTONES
# =========================
        botones = tk.Frame(ventana)
        botones.pack(pady=10)

        ttk.Button(
            botones,
            text="➕ Registrar",
            width=14,
            style="Icono.TButton",
            command=self.registrar
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            botones,
            text="🔍 Consultar",
            width=14,
            style="Icono.TButton",
            command=self.consultar
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            botones,
            text="✏ Actualizar",
            width=14,
            style="Icono.TButton",
            command=self.actualizar
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            botones,
            text="🗑 Eliminar",
            width=14,
            style="Icono.TButton",
            command=self.eliminar
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            botones,
            text="📊 Exportar Excel",
            width=16,
            style="Icono.TButton",
            command=self.exportar_excel_clientes
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            botones,
            text="📄 Exportar PDF",
            width=16,
            style="Icono.TButton",
            command=self.exportar_pdf_clientes
        ).grid(row=0, column=5, padx=5)

        ttk.Button(
            botones,
            text="🌓 Tema",
            width=12,
            style="Icono.TButton",
            command=self.cambiar_tema
        ).grid(row=0, column=6, padx=5)

# =========================
# TABLA
# =========================
        tabla_frame = tk.Frame(ventana)
        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=(
                "codigo",
                "nombre",
                "telefono",
                "tipo",
                "imagen"
            ),
            show="headings"
        )

        self.tabla.heading("codigo", text="Codigo")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("telefono", text="Telefono")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("imagen", text="Imagen")

        self.tabla.column("codigo", width=100)
        self.tabla.column("nombre", width=220)
        self.tabla.column("telefono", width=150)
        self.tabla.column("tipo", width=150)
        self.tabla.column("imagen", width=160)

        self.tabla.pack(
            fill="both",
            expand=True
        )

# Seleccionar una fila
        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar
        )

# Cargar datos
        self.mostrar_datos()

# Aplicar el tema claro/oscuro guardado (se mantiene entre modulos)
        aplicar_tema(
            self.ventana,
            self.estilo,
            excluir_widgets=[self.label_imagen]
        )
        self.label_imagen.config(bg="white", fg="black")

    def cambiar_tema(self):

        alternar_tema()

        aplicar_tema(
            self.ventana,
            self.estilo,
            excluir_widgets=[self.label_imagen]
        )
        self.label_imagen.config(bg="white", fg="black")

# =========================
# IMAGENES (PILLOW)
# =========================
    def seleccionar_imagen(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen del cliente",
            filetypes=[
                ("Imagenes JPG/PNG", "*.jpg *.jpeg *.png"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            return

        extension = os.path.splitext(ruta)[1].lower()

        if extension not in EXTENSIONES_PERMITIDAS:
            messagebox.showwarning(
                "Formato invalido",
                "Solo se permiten imagenes en formato JPG o PNG."
            )
            return

        tamano = os.path.getsize(ruta)

        if tamano > TAMANO_MAXIMO_BYTES:
            messagebox.showwarning(
                "Imagen muy pesada",
                f"La imagen no debe superar los {TAMANO_MAXIMO_MB} MB."
            )
            return

        try:
            imagen = Image.open(ruta)
            imagen.verify()
        except Exception:
            messagebox.showerror(
                "Error",
                "El archivo seleccionado no es una imagen valida."
            )
            return

        self.ruta_imagen_nueva = ruta
        self.mostrar_vista_previa(ruta)

    def quitar_imagen(self):

        self.ruta_imagen_nueva = "QUITAR"
        self.nombre_imagen_actual = None
        self.imagen_tk = None

        self.label_imagen.config(
            image="",
            text="Sin imagen"
        )

    def descargar_imagen(self):

        if not self.nombre_imagen_actual:
            messagebox.showwarning(
                "Descargar",
                "Este cliente no tiene una imagen guardada."
            )
            return

        ruta_origen = os.path.join(
            CARPETA_IMAGENES,
            self.nombre_imagen_actual
        )

        if not os.path.exists(ruta_origen):
            messagebox.showerror(
                "Error",
                "No se encontro el archivo de imagen en el servidor."
            )
            return

        ruta_destino = filedialog.asksaveasfilename(
            title="Guardar imagen como",
            defaultextension=".jpg",
            initialfile=self.nombre_imagen_actual,
            filetypes=[
                ("Imagen JPG", "*.jpg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta_destino:
            return

        try:
            shutil.copy2(ruta_origen, ruta_destino)

            messagebox.showinfo(
                "Descargar",
                "Imagen descargada correctamente."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo descargar la imagen.\n\n{e}"
            )

    def mostrar_vista_previa(self, ruta_o_archivo):

        try:
            imagen = Image.open(ruta_o_archivo).convert("RGB")
            imagen.thumbnail(DIMENSION_MINIATURA, Image.LANCZOS)

            self.imagen_tk = ImageTk.PhotoImage(imagen)

            self.label_imagen.config(
                image=self.imagen_tk,
                text=""
            )

        except Exception:
            self.label_imagen.config(
                image="",
                text="Sin imagen"
            )

    def procesar_imagen(self, codigo):
        """
        Redimensiona, aplica un filtro de nitidez y convierte
        la imagen seleccionada a JPG estandarizado. Devuelve el
        nombre de archivo a guardar en la base de datos, o None
        si no hay imagen.
        """

        if self.ruta_imagen_nueva == "QUITAR":
            return None

        if self.ruta_imagen_nueva is None:
            return self.nombre_imagen_actual

        try:
            imagen = Image.open(self.ruta_imagen_nueva).convert("RGB")

            imagen.thumbnail(
                (DIMENSION_MAXIMA, DIMENSION_MAXIMA),
                Image.LANCZOS
            )

            imagen = imagen.filter(ImageFilter.SHARPEN)

            nombre_archivo = f"cliente_{codigo}.jpg"
            ruta_destino = os.path.join(
                CARPETA_IMAGENES,
                nombre_archivo
            )

            imagen.save(ruta_destino, "JPEG", quality=85)

            return nombre_archivo

        except Exception as e:
            messagebox.showerror(
                "Error de imagen",
                f"No se pudo procesar la imagen.\n\n{e}"
            )
            return self.nombre_imagen_actual

# =========================
# REGISTRAR
# =========================
    def registrar(self):

        if not self.codigo.get() or not self.nombre.get() or not self.telefono.get() or not self.tipo.get():
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar todos los campos."
            )
            return

        if not self.codigo.get().strip().isdigit():
            messagebox.showwarning(
                "Codigo invalido",
                "El campo Codigo solo debe contener digitos (0-9)."
            )
            return

        if not self.telefono.get().strip().isdigit():
            messagebox.showwarning(
                "Telefono invalido",
                "El campo Telefono solo debe contener digitos (0-9)."
            )
            return

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                nombre_archivo_imagen = self.procesar_imagen(
                    self.codigo.get().strip()
                )

                sql = """
                    INSERT INTO clientes
                    (codigo, nombre, telefono, tipo, foto)
                    VALUES (%s, %s, %s, %s, %s)
                """

                datos = (
                    self.codigo.get(),
                    self.nombre.get(),
                    self.telefono.get(),
                    self.tipo.get(),
                    nombre_archivo_imagen
                )

                cursor.execute(sql, datos)
                conexion.commit()

                messagebox.showinfo(
                    "Correcto",
                    "Cliente registrado correctamente."
                )

                self.limpiar()
                self.mostrar_datos()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e)
                )

            finally:
                cursor.close()
                conexion.close()

# =========================
# CONSULTAR
# =========================
    def consultar(self):

        texto = self.buscar.get().strip()

        if not texto:
            self.mostrar_datos()
            return

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                sql = """
                    SELECT codigo, nombre, telefono, tipo, foto
                    FROM clientes
                    WHERE CAST(codigo AS CHAR) LIKE %s
                    OR nombre LIKE %s
                    OR telefono LIKE %s
                    OR tipo LIKE %s
                """

                parametro = "%" + texto + "%"

                cursor.execute(
                    sql,
                    (
                        parametro,
                        parametro,
                        parametro,
                        parametro
                    )
                )

                registros = cursor.fetchall()

                for registro in registros:
                    codigo_r, nombre_r, telefono_r, tipo_r, foto_r = registro

                    self.fotos_cache[str(codigo_r)] = foto_r

                    self.tabla.insert(
                        "",
                        "end",
                        values=(
                            codigo_r,
                            nombre_r,
                            telefono_r,
                            tipo_r,
                            foto_r if foto_r else "Sin imagen"
                        )
                    )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e)
                )

            finally:
                cursor.close()
                conexion.close()

# =========================
# ACTUALIZAR
# =========================
    def actualizar(self):

        if not self.codigo.get() or not self.nombre.get() or not self.telefono.get() or not self.tipo.get():
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar todos los campos."
            )
            return

        if not self.codigo.get().strip().isdigit():
            messagebox.showwarning(
                "Codigo invalido",
                "El campo Codigo solo debe contener digitos (0-9)."
            )
            return

        if not self.telefono.get().strip().isdigit():
            messagebox.showwarning(
                "Telefono invalido",
                "El campo Telefono solo debe contener digitos (0-9)."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea actualizar los datos de este cliente?"
        )

        if not confirmar:
            return

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                nombre_archivo_imagen = self.procesar_imagen(
                    self.codigo.get().strip()
                )

                sql = """
                    UPDATE clientes
                    SET nombre=%s,
                        telefono=%s,
                        tipo=%s,
                        foto=%s
                    WHERE codigo=%s
                """

                datos = (
                    self.nombre.get(),
                    self.telefono.get(),
                    self.tipo.get(),
                    nombre_archivo_imagen,
                    self.codigo.get()
                )

                cursor.execute(sql, datos)
                conexion.commit()

                messagebox.showinfo(
                    "Correcto",
                    "Cliente actualizado correctamente."
                )

                self.limpiar()
                self.mostrar_datos()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e)
                )

            finally:
                cursor.close()
                conexion.close()

# =========================
# ELIMINAR
# =========================
    def eliminar(self):

        if not self.codigo.get():
            messagebox.showwarning(
                "Aviso",
                "Seleccione un cliente de la tabla."
            )
            return

        if not self.codigo.get().strip().isdigit():
            messagebox.showwarning(
                "Codigo invalido",
                "El campo Codigo solo debe contener digitos (0-9)."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Desea eliminar este cliente?"
        )

        if not confirmar:
            return

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                sql = """
                    DELETE FROM clientes
                    WHERE codigo=%s
                """

                cursor.execute(
                    sql,
                    (self.codigo.get(),)
                )

                conexion.commit()

                messagebox.showinfo(
                    "Correcto",
                    "Cliente eliminado correctamente."
                )

                self.limpiar()
                self.mostrar_datos()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e)
                )

            finally:
                cursor.close()
                conexion.close()

# =========================
# MOSTRAR DATOS
# =========================
    def mostrar_datos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT codigo, nombre, telefono, tipo, foto
                    FROM clientes
                    """
                )

                registros = cursor.fetchall()

                for registro in registros:
                    codigo_r, nombre_r, telefono_r, tipo_r, foto_r = registro

                    self.fotos_cache[str(codigo_r)] = foto_r

                    self.tabla.insert(
                        "",
                        "end",
                        values=(
                            codigo_r,
                            nombre_r,
                            telefono_r,
                            tipo_r,
                            foto_r if foto_r else "Sin imagen"
                        )
                    )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e)
                )

            finally:
                cursor.close()
                conexion.close()

# =========================
# SELECCIONAR
# =========================
    def seleccionar(self, evento):

        seleccion = self.tabla.selection()

        if seleccion:

            datos = self.tabla.item(
                seleccion[0],
                "values"
            )

            self.codigo.delete(0, tk.END)
            self.nombre.delete(0, tk.END)
            self.telefono.delete(0, tk.END)

            self.codigo.insert(0, datos[0])
            self.nombre.insert(0, datos[1])
            self.telefono.insert(0, datos[2])

            self.tipo.set(datos[3])

            self.ruta_imagen_nueva = None
            self.nombre_imagen_actual = self.fotos_cache.get(
                str(datos[0])
            )

            if self.nombre_imagen_actual:
                ruta_guardada = os.path.join(
                    CARPETA_IMAGENES,
                    self.nombre_imagen_actual
                )

                if os.path.exists(ruta_guardada):
                    self.mostrar_vista_previa(ruta_guardada)
                else:
                    self.label_imagen.config(image="", text="Sin imagen")
            else:
                self.label_imagen.config(image="", text="Sin imagen")

# =========================
# EXPORTAR
# =========================
    def obtener_datos_exportacion(self):

        texto = self.buscar.get().strip()

        conexion = conectar()

        if conexion is None:
            return []

        try:
            cursor = conexion.cursor()

            sql = """
                SELECT codigo, nombre, telefono, tipo
                FROM clientes
                WHERE 1=1
            """

            parametros = []

            if texto:
                sql += """
                    AND (
                        CAST(codigo AS CHAR) LIKE %s
                        OR nombre LIKE %s
                        OR telefono LIKE %s
                        OR tipo LIKE %s
                    )
                """

                parametro = "%" + texto + "%"

                parametros.extend([
                    parametro,
                    parametro,
                    parametro,
                    parametro
                ])

            cursor.execute(
                sql,
                parametros
            )

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()


    def exportar_excel_clientes(self):

        datos = self.obtener_datos_exportacion()

        if not datos:
            messagebox.showwarning(
                "Exportar",
                "No hay datos para exportar."
            )
            return

        exportar_excel(
            "Clientes",
            [
                "Codigo",
                "Nombre",
                "Telefono",
                "Tipo"
            ],
            datos
        )


    def exportar_pdf_clientes(self):

        datos = self.obtener_datos_exportacion()

        if not datos:
            messagebox.showwarning(
                "Exportar",
                "No hay datos para exportar."
            )
            return

        exportar_pdf(
            "Clientes",
            [
                "Codigo",
                "Nombre",
                "Telefono",
                "Tipo"
            ],
            datos
        )

# =========================
# LIMPIAR
# =========================
    def limpiar(self):

        self.codigo.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.tipo.set("")
        self.buscar.delete(0, tk.END)

        self.ruta_imagen_nueva = None
        self.nombre_imagen_actual = None
        self.imagen_tk = None
        self.label_imagen.config(image="", text="Sin imagen")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = ModuloClientes(ventana)
    ventana.mainloop()
