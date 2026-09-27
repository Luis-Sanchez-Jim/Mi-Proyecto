import tkinter as tk
from tkinter import ttk, messagebox

from conexion import conectar
from exportar import exportar_excel, exportar_pdf
from tema import aplicar_tema, alternar_tema


class ModuloVehiculos:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de Vehiculos")
        self.ventana.geometry("900x650")

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
            text="Gestion de Vehiculos",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        # Formulario
        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)

        tk.Label(formulario, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
        self.placa = tk.Entry(formulario, width=30)
        self.placa.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        self.tipo = ttk.Combobox(
            formulario,
            width=28,
            state="readonly",
            values=[
                "Patrulla",
                "Motocicleta",
                "Camioneta",
                "Automovil"
            ]
        )
        self.tipo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Modelo:").grid(row=2, column=0, padx=5, pady=5)
        self.modelo = tk.Entry(formulario, width=30)
        self.modelo.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Estado:").grid(row=3, column=0, padx=5, pady=5)
        self.estado = ttk.Combobox(
            formulario,
            width=28,
            state="readonly",
            values=[
                "Disponible",
                "En servicio",
                "Mantenimiento"
            ]
        )
        self.estado.grid(row=3, column=1, padx=5, pady=5)

        # Busqueda
        tk.Label(self.ventana, text="Buscar:").pack()

        self.buscar = tk.Entry(self.ventana, width=40)
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
            command=self.exportar_excel_vehiculos
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            botones,
            text="📄 Exportar PDF",
            width=16,
            style="Icono.TButton",
            command=self.exportar_pdf_vehiculos
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
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=("placa", "tipo", "modelo", "estado"),
            show="headings"
        )

        self.tabla.heading("placa", text="Placa")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("modelo", text="Modelo")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("placa", width=120)
        self.tabla.column("tipo", width=180)
        self.tabla.column("modelo", width=200)
        self.tabla.column("estado", width=180)

        self.tabla.pack(fill="both", expand=True)

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

    # -----------------------------
    # MOSTRAR DATOS
    # -----------------------------
    def mostrar_datos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conexion = conectar()

        if conexion is None:
            return

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT placa, tipo, modelo, estado
            FROM vehiculos
        """)

        registros = cursor.fetchall()

        for registro in registros:
            self.tabla.insert("", "end", values=registro)

        cursor.close()
        conexion.close()

    # -----------------------------
    # REGISTRAR
    # -----------------------------
    def registrar(self):

        placa = self.placa.get().strip()
        tipo = self.tipo.get().strip()
        modelo = self.modelo.get().strip()
        estado = self.estado.get().strip()

        if not placa or not tipo or not modelo or not estado:
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar todos los campos."
            )
            return

        conexion = conectar()

        if conexion is None:
            return

        try:
            cursor = conexion.cursor()

            sql = """
                INSERT INTO vehiculos
                (placa, tipo, modelo, estado)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (placa, tipo, modelo, estado)
            )

            conexion.commit()

            messagebox.showinfo(
                "Registro",
                "Vehiculo registrado correctamente."
            )

            self.limpiar()
            self.mostrar_datos()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo registrar el vehiculo.\n\n{e}"
            )

        finally:
            cursor.close()
            conexion.close()

    # -----------------------------
    # CONSULTAR
    # -----------------------------
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
                SELECT placa, tipo, modelo, estado
                FROM vehiculos
                WHERE placa LIKE %s
                OR tipo LIKE %s
                OR modelo LIKE %s
                OR estado LIKE %s
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

    # -----------------------------
    # ACTUALIZAR
    # -----------------------------
    def actualizar(self):

        placa = self.placa.get().strip()
        tipo = self.tipo.get().strip()
        modelo = self.modelo.get().strip()
        estado = self.estado.get().strip()

        if not placa or not tipo or not modelo or not estado:
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar todos los campos."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea actualizar los datos de este vehiculo?"
        )

        if not confirmar:
            return

        conexion = conectar()

        if conexion is None:
            return

        try:
            cursor = conexion.cursor()

            sql = """
                UPDATE vehiculos
                SET tipo = %s,
                    modelo = %s,
                    estado = %s
                WHERE placa = %s
            """

            cursor.execute(
                sql,
                (tipo, modelo, estado, placa)
            )

            conexion.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Actualizar",
                    "No se encontro un vehiculo con esa placa."
                )
            else:
                messagebox.showinfo(
                    "Actualizar",
                    "Vehiculo actualizado correctamente."
                )

            self.limpiar()
            self.mostrar_datos()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el vehiculo.\n\n{e}"
            )

        finally:
            cursor.close()
            conexion.close()

    # -----------------------------
    # ELIMINAR
    # -----------------------------
    def eliminar(self):

        placa = self.placa.get().strip()

        if not placa:
            messagebox.showwarning(
                "Eliminar",
                "Ingrese la placa del vehiculo."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este vehiculo?"
        )

        if not confirmar:
            return

        conexion = conectar()

        if conexion is None:
            return

        try:
            cursor = conexion.cursor()

            cursor.execute(
                "DELETE FROM vehiculos WHERE placa = %s",
                (placa,)
            )

            conexion.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Eliminar",
                    "No se encontro un vehiculo con esa placa."
                )
            else:
                messagebox.showinfo(
                    "Eliminar",
                    "Vehiculo eliminado correctamente."
                )

            self.limpiar()
            self.mostrar_datos()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el vehiculo.\n\n{e}"
            )

        finally:
            cursor.close()
            conexion.close()

    # -----------------------------
    # SELECCIONAR FILA
    # -----------------------------
    def seleccionar(self, evento):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.placa.delete(0, tk.END)
        self.placa.insert(0, valores[0])

        self.tipo.set(valores[1])

        self.modelo.delete(0, tk.END)
        self.modelo.insert(0, valores[2])

        self.estado.set(valores[3])

    # -----------------------------
    # EXPORTAR (usa lo que esta en la tabla)
    # -----------------------------
    def obtener_datos_tabla(self):

        datos = []

        for fila in self.tabla.get_children():
            datos.append(self.tabla.item(fila, "values"))

        return datos

    def exportar_excel_vehiculos(self):

        datos = self.obtener_datos_tabla()

        if not datos:
            messagebox.showwarning(
                "Exportar",
                "No hay datos para exportar."
            )
            return

        exportar_excel(
            "Vehiculos",
            [
                "Placa",
                "Tipo",
                "Modelo",
                "Estado"
            ],
            datos
        )

    def exportar_pdf_vehiculos(self):

        datos = self.obtener_datos_tabla()

        if not datos:
            messagebox.showwarning(
                "Exportar",
                "No hay datos para exportar."
            )
            return

        exportar_pdf(
            "Vehiculos",
            [
                "Placa",
                "Tipo",
                "Modelo",
                "Estado"
            ],
            datos
        )

    # -----------------------------
    # LIMPIAR
    # -----------------------------
    def limpiar(self):

        self.placa.delete(0, tk.END)
        self.tipo.set("")
        self.modelo.delete(0, tk.END)
        self.estado.set("")
        self.buscar.delete(0, tk.END)


if __name__ == "__main__":

    root = tk.Tk()

    ModuloVehiculos(root)

    root.mainloop()
