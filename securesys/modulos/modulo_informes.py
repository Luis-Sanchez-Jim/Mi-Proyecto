import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from conexion import conectar
from exportar import exportar_excel, exportar_pdf
from tema import aplicar_tema, alternar_tema


class ModuloInformes:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de Informes")
        self.ventana.geometry("950x650")
        estilo = ttk.Style()
        estilo.configure(
            "Icono.TButton",
            font=("Segoe UI Emoji", 10),
            padding=6
        )
        self.estilo = estilo

# Titulo
        titulo = tk.Label(
            self.ventana,
            text="Gestion de Informes",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

# Formulario
        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)

# Numero
        tk.Label(
            formulario,
            text="Numero:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.numero = tk.Entry(
            formulario,
            width=30
        )
        self.numero.grid(row=0, column=1, padx=5, pady=5)

# Cliente
        tk.Label(
            formulario,
            text="Cliente:"
        ).grid(row=1, column=0, padx=5, pady=5)
        self.cliente = tk.Entry(
            formulario,
            width=30,
            fg="gray"
        )
        self.cliente.insert(0, "CODIGO DE CLIENTE")
        self.cliente.grid(row=1, column=1, padx=5, pady=5)

        self.cliente.bind(
            "<FocusIn>",
            self.quitar_placeholder_cliente
        )
        self.cliente.bind(
            "<FocusOut>",
            self.poner_placeholder_cliente
        )

# Fecha
        tk.Label(
            formulario,
            text="Fecha:"
        ).grid(row=2, column=0, padx=5, pady=5)
        self.fecha = DateEntry(
            formulario,
            width=27,
            date_pattern="yyyy-mm-dd",
            locale="es",
            firstweekday="monday",
            showweeknumbers=False,
            showothermonthdays=True,
            selectmode="day"
        )
        self.fecha.grid(row=2, column=1, padx=5, pady=5)

# Observaciones
        tk.Label(
            formulario,
            text="Observaciones:"
        ).grid(row=3, column=0, padx=5, pady=5)
        self.observaciones = tk.Entry(
            formulario,
            width=30
        )
        self.observaciones.grid(row=3, column=1, padx=5, pady=5)

# Busqueda
        tk.Label(
            self.ventana,
            text="Buscar:"
        ).pack()
        self.buscar = tk.Entry(
            self.ventana,
            width=40
        )
        self.buscar.pack(pady=5)

# Botones
        botones = tk.Frame(self.ventana)
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
            command=self.exportar_excel_informes
        ).grid(row=0, column=4, padx=5)
        ttk.Button(
            botones,
            text="📄 Exportar PDF",
            width=16,
            style="Icono.TButton",
            command=self.exportar_pdf_informes
        ).grid(row=0, column=5, padx=5)
        ttk.Button(
            botones,
            text="🌓 Tema",
            width=12,
            style="Icono.TButton",
            command=self.cambiar_tema
        ).grid(row=0, column=6, padx=5)

# Tabla
        tabla_frame = tk.Frame(self.ventana)
        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=(
                "numero",
                "cliente",
                "fecha",
                "observaciones"
            ),
            show="headings"
        )
        self.tabla.heading(
            "numero",
            text="Numero"
        )
        self.tabla.heading(
            "cliente",
            text="Cliente"
        )
        self.tabla.heading(
            "fecha",
            text="Fecha"
        )
        self.tabla.heading(
            "observaciones",
            text="Observaciones"
        )
        self.tabla.column(
            "numero",
            width=100
        )
        self.tabla.column(
            "cliente",
            width=100
        )
        self.tabla.column(
            "fecha",
            width=120
        )
        self.tabla.column(
            "observaciones",
            width=400
        )
        self.tabla.pack(
            fill="both",
            expand=True
        )
        self.tabla.bind(
            "<ButtonRelease-1>",
            self.seleccionar
        )
        self.mostrar_datos()

# Aplicar el tema claro/oscuro guardado (se mantiene entre modulos)
        aplicar_tema(self.ventana, self.estilo)
    def cambiar_tema(self):
        alternar_tema()
        aplicar_tema(self.ventana, self.estilo)

# --------------------------------
# MOSTRAR DATOS
# --------------------------------
    def mostrar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        conexion = conectar()
        if conexion is None:
            return
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT numero, cliente, fecha, observaciones
            FROM informes
        """)
        registros = cursor.fetchall()
        for registro in registros:
            self.tabla.insert(
                "",
                "end",
                values=registro
            )
        cursor.close()
        conexion.close()

# --------------------------------
# REGISTRAR
# --------------------------------
    def registrar(self):
        numero = self.numero.get().strip()
        cliente = self.cliente.get().strip()
        fecha = self.fecha.get().strip()
        observaciones = self.observaciones.get().strip()
        if cliente == "CODIGO DE CLIENTE":
            cliente = ""
        if not numero or not cliente or not fecha or not observaciones:
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar todos los campos."
            )
            return
        if not numero.isdigit():
            messagebox.showwarning(
                "Numero invalido",
                "El campo Numero solo debe contener digitos (0-9)."
            )
            return
        conexion = conectar()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO informes
                (numero, cliente, fecha, observaciones)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    numero,
                    cliente,
                    fecha,
                    observaciones
                )
            )
            conexion.commit()
            messagebox.showinfo(
                "Registro",
                "Informe registrado correctamente."
            )
            self.limpiar()
            self.mostrar_datos()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo registrar el informe.\n\n{e}"
            )
        finally:
            cursor.close()
            conexion.close()

# --------------------------------
# CONSULTAR
# --------------------------------
    def consultar(self):
        texto = self.buscar.get().strip()
        if not texto:
            self.mostrar_datos()
            return
        conexion = conectar()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            sql = """
                SELECT numero, cliente, fecha, observaciones
                FROM informes
                WHERE CAST(numero AS CHAR) LIKE %s
                OR CAST(cliente AS CHAR) LIKE %s
                OR CAST(fecha AS CHAR) LIKE %s
                OR observaciones LIKE %s
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
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            for registro in registros:
                self.tabla.insert(
                    "",
                    "end",
                    values=registro
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo realizar la consulta.\n\n{e}"
            )
        finally:
            cursor.close()
            conexion.close()

# --------------------------------
# ACTUALIZAR
# --------------------------------
    def actualizar(self):
        numero = self.numero.get().strip()
        cliente = self.cliente.get().strip()
        fecha = self.fecha.get().strip()
        observaciones = self.observaciones.get().strip()
        if cliente == "CODIGO DE CLIENTE":
            cliente = ""
        if not numero or not cliente or not fecha or not observaciones:
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar todos los campos."
            )
            return
        if not numero.isdigit():
            messagebox.showwarning(
                "Numero invalido",
                "El campo Numero solo debe contener digitos (0-9)."
            )
            return
        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea actualizar los datos de este informe?"
        )
        if not confirmar:
            return
        conexion = conectar()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE informes
                SET cliente = %s,
                    fecha = %s,
                    observaciones = %s
                WHERE numero = %s
            """
            cursor.execute(
                sql,
                (
                    cliente,
                    fecha,
                    observaciones,
                    numero
                )
            )
            conexion.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Actualizar",
                    "No se encontro un informe con ese numero."
                )
            else:
                messagebox.showinfo(
                    "Actualizar",
                    "Informe actualizado correctamente."
                )
            self.limpiar()
            self.mostrar_datos()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el informe.\n\n{e}"
            )
        finally:
            cursor.close()
            conexion.close()

# --------------------------------
# ELIMINAR
# --------------------------------
    def eliminar(self):
        numero = self.numero.get().strip()
        if not numero:
            messagebox.showwarning(
                "Eliminar",
                "Ingrese el numero del informe."
            )
            return
        if not numero.isdigit():
            messagebox.showwarning(
                "Numero invalido",
                "El campo Numero solo debe contener digitos (0-9)."
            )
            return
        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este informe?"
        )
        if not confirmar:
            return
        conexion = conectar()
        if conexion is None:
            return
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "DELETE FROM informes WHERE numero = %s",
                (numero,)
            )
            conexion.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Eliminar",
                    "No se encontro un informe con ese numero."
                )
            else:
                messagebox.showinfo(
                    "Eliminar",
                    "Informe eliminado correctamente."
                )
            self.limpiar()
            self.mostrar_datos()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el informe.\n\n{e}"
            )
        finally:
            cursor.close()
            conexion.close()

# --------------------------------
# SELECCIONAR FILA
# --------------------------------
    def seleccionar(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(
            seleccion[0],
            "values"
        )
        self.numero.delete(0, tk.END)
        self.numero.insert(0, valores[0])
        self.cliente.delete(0, tk.END)
        self.cliente.config(fg="black")
        self.cliente.insert(0, valores[1])
        try:
            self.fecha.set_date(
                datetime.strptime(str(valores[2]), "%Y-%m-%d")
            )
        except ValueError:
            pass
        self.observaciones.delete(0, tk.END)
        self.observaciones.insert(0, valores[3])
    def quitar_placeholder_cliente(self, evento):
        if self.cliente.get() == "CODIGO DE CLIENTE":
            self.cliente.delete(0, tk.END)
            self.cliente.config(fg="black")
    def poner_placeholder_cliente(self, evento):
        if not self.cliente.get():
            self.cliente.insert(0, "CODIGO DE CLIENTE")
            self.cliente.config(fg="gray")

# --------------------------------
# EXPORTAR (usa lo que esta en la tabla)
# --------------------------------
    def obtener_datos_tabla(self):
        datos = []
        for fila in self.tabla.get_children():
            datos.append(self.tabla.item(fila, "values"))
        return datos
    def exportar_excel_informes(self):
        datos = self.obtener_datos_tabla()
        if not datos:
            messagebox.showwarning(
                "Exportar",
                "No hay datos para exportar."
            )
            return
        exportar_excel(
            "Informes",
            [
                "Numero",
                "Cliente",
                "Fecha",
                "Observaciones"
            ],
            datos
        )
    def exportar_pdf_informes(self):
        datos = self.obtener_datos_tabla()
        if not datos:
            messagebox.showwarning(
                "Exportar",
                "No hay datos para exportar."
            )
            return

        exportar_pdf(
            "Informes",
            [
                "Numero",
                "Cliente",
                "Fecha",
                "Observaciones"
            ],
            datos
        )   

# --------------------------------
# LIMPIAR
# --------------------------------
    def limpiar(self):
        self.numero.delete(0, tk.END)
        self.cliente.delete(0, tk.END)
        self.cliente.insert(0, "CODIGO DE CLIENTE")
        self.cliente.config(fg="gray")
        self.fecha.set_date(datetime.now())
        self.observaciones.delete(0, tk.END)
        self.buscar.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    ModuloInformes(root)
    root.mainloop()