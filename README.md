## Características

- **CRUD completo** (Registrar, Consultar, Actualizar, Eliminar) en los 4 módulos.
- **Confirmación** antes de actualizar o eliminar registros.
- **Validación de campos numéricos** (código, teléfono, número de informe) — rechaza letras y símbolos.
- **Búsqueda** en tiempo real por cualquier campo visible de cada tabla.
- **Exportación a Excel y PDF** con formato profesional (`openpyxl` y `reportlab`).
- **Gestión de imágenes** en Clientes y Dispositivos:
  - Selección desde el explorador de archivos (solo JPG/PNG, máx. 5 MB).
  - Quitar una imagen Seleccionada
  - Descarga de la imagen cargada en la base de datos.
- **Selector de fecha con calendario** (`tkcalendar`) en el módulo de Informes.
- **Temas claro/oscuro** intercambiables, con el tema elegido persistiendo entre módulos y entre reinicios de la aplicación.
- **Iconografía consistente** en todos los botones (`ttk.Button` + íconos).

---

## Requisitos

- Python 3.10 o superior
- MySQL Server (local o remoto)
- Librerías de Python 

```bash
pip install mysql-connector-python
pip install Pillow
pip install tkcalendar
pip install openpyxl
pip install reportlab
```

-tkinter viene incluido con Python en Windows

## Estructura del proyecto

```
SecureSys/
├── Menu_Inicial.py         # Punto de entrada: menú principal
├── requirements.txt        # Dependencias del proyecto
├── conexion.py             # Conexión a la base de datos MySQL
├── exportar.py             # Funciones de exportacion a Excel y PDF
├── tema.py                 # Sistema de temas claro/oscuro (persistente)
├── tema_config.json        # Se crea automaticamente al elegir un tema
├── imagenes_clientes/      # Se crea automaticamente al guardar fotos de clientes
├── imagenes_dispositivos/  # Se crea automaticamente al guardar fotos de dispositivos
└── modulos/
    ├── modulo_clientes.py
    ├── modulo_vehiculos.py
    ├── modulo_dispositivos.py
    └── modulo_informes.py
```

## Configuración de la base de datos

1. Crea la base de datos:

```sql
CREATE DATABASE securesys;
USE securesys;
```

2. Crea las tablas:

```sql
CREATE TABLE clientes (
    codigo    INT PRIMARY KEY,
    nombre    VARCHAR(100) NOT NULL,
    telefono  VARCHAR(20)  NOT NULL,
    tipo      VARCHAR(30)  NOT NULL,
    foto      VARCHAR(255) NULL
);

CREATE TABLE vehiculos (
    placa   VARCHAR(15) PRIMARY KEY,
    tipo    VARCHAR(30) NOT NULL,
    modelo  VARCHAR(50) NOT NULL,
    estado  VARCHAR(30) NOT NULL
);

CREATE TABLE dispositivos (
    codigo     INT PRIMARY KEY,
    tipo       VARCHAR(30)  NOT NULL,
    estado     VARCHAR(30)  NOT NULL,
    ubicacion  VARCHAR(100) NOT NULL,
    foto       VARCHAR(255) NULL
);

CREATE TABLE informes (
    numero         INT PRIMARY KEY,
    cliente        INT NOT NULL,
    fecha          DATE NOT NULL,
    observaciones  VARCHAR(255) NOT NULL,
    CONSTRAINT informes_ibfk_1 FOREIGN KEY (cliente) REFERENCES clientes (codigo)
);
```

> El campo **Cliente** en Informes guarda el **código numérico** de un cliente ya registrado (no su nombre), por la relación de llave foránea con `clientes.codigo`.

3. Ajusta las credenciales de conexión en `conexion.py` si es necesario (usuario, contraseña, host, puerto).

---

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python Menu_Inicial.py
```

Se abrirá el menú principal, desde donde se accede a cada módulo (Clientes, Vehículos, Dispositivos, Informes) en su propia ventana.

---

## Uso rápido

| Acción | Cómo hacerlo |
|---|---|
| Registrar | Completa el formulario y presiona **➕ Registrar** |
| Buscar | Escribe en el campo **Buscar** y presiona **🔍 Consultar** (vacío = mostrar todo) |
| Editar | Selecciona una fila de la tabla, modifica los campos y presiona **✏ Actualizar** |
| Eliminar | Selecciona una fila y presiona **🗑 Eliminar** (pide confirmación) |
| Exportar | Presiona **📊 Exportar Excel** o **📄 Exportar PDF** — exporta lo que esté visible en la tabla en ese momento (respeta la última búsqueda) |
| Cambiar tema | Presiona **🌓 Tema** en cualquier módulo, o **🌓 Cambiar Tema** en el menú principal |
| Adjuntar foto (Clientes/Dispositivos) | **🖼 Seleccionar Imagen** → elige un JPG/PNG → guarda con Registrar/Actualizar |

---

## Notas

- Las imágenes se guardan localmente en `imagenes_clientes/` e `imagenes_dispositivos/´
- El tema seleccionado se guarda en `tema_config.json`, en la raíz del proyecto.
- La exportación a Excel/PDF de Vehículos, Clientes, Informes y Dispositivos toma los datos **tal como se muestran en la tabla**.
