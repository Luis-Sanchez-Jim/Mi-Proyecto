import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="securesys",
            connection_timeout=5,
            use_pure=True
        )
        if conexion.is_connected():
            print("Conexion exitosa con la base de datos")
            return conexion
    except mysql.connector.Error as e:
        print("Error de conexion:", e)
    return None
if __name__ == "__main__":
    bd = conectar()

    if bd:
        bd.close()
        print("Conexion cerrada correctamente")