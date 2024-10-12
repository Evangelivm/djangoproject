# API de Gestion de Empleados

Este proyecto es una API que utiliza PostgreSQL como base de datos y cuenta con documentación generada automáticamente con Swagger.

## Requisitos

- Python 3.12
- PostgreSQL

## Instalación

1. **Clonar el repositorio**

   Clona el repositorio en tu máquina local.

   ```bash
   git clone https://github.com/Evangelivm/djangoproject
   cd djangoproject
   ```

2. **Crear un entorno virtual**

   Instala y configura un entorno virtual para aislar las dependencias del proyecto.

   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**

   Activa el entorno virtual que acabas de crear.

   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**

   Instala las dependencias del proyecto especificadas en el archivo `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

   > **Nota:** Debes instalar las dependencias antes de ejecutar el servidor.

5. **Configurar base de datos**

   Crea una base de datos PostgreSQL en tu sistema.

6. **Crear archivo `.env`**

   Crea un archivo `.env` en el directorio raíz del proyecto y define los siguientes parámetros para conectarte a la base de datos:

   ```env
   API_NAME = <nombre-de-su-base-de-datos>
   API_USER = <usuario-de-su-base-de-datos>
   API_PASSWORD = <contraseña-de-su-base-de-datos>
   API_HOST = localhost
   API_PORT = 5432
   ```

7. **Crear tablas y datos iniciales**

   Ejecuta el script `create_tables.py` para crear las tablas y cargar los datos iniciales.

   ```bash
   py create_tables.py
   ```

8. **Iniciar el servidor**

   Ejecuta el servidor con el siguiente comando:

   ```bash
   py manage.py runserver 3000
   ```

9. **Acceder a la documentación de la API**

   Una vez que el servidor esté en ejecución, puedes acceder a la documentación generada por Swagger en la siguiente ruta:

   [http://localhost:3000/api/swagger/](http://localhost:3000/api/swagger/)

## Notas adicionales

- Asegúrate de haber instalado los `requirements.txt` antes de ejecutar el servidor.
- Verifica que PostgreSQL esté en funcionamiento y configurado correctamente en tu máquina.
