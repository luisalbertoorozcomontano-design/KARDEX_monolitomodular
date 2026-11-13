# KARDEX Agrícola — interfaz web integrada

Esta versión incorpora una interfaz web adaptable a computadoras y móviles, servida por FastAPI en la misma dirección que la API.

## Ejecutar con Docker (recomendado)

1. Instalar Docker Desktop y asegurarse de que esté iniciado.
2. Abrir una terminal en la carpeta `KARDEX_monolitomodular`.
3. Ejecutar:

   ```bash
   docker compose up --build
   ```

4. Abrir:
   - Aplicación: http://localhost:8001/
   - Documentación de API: http://localhost:8001/docs
   - phpMyAdmin: http://localhost:8080/

Para detener los servicios: `docker compose down`.

## Ejecutar sin Docker

1. Crear y activar un entorno virtual de Python.
2. Instalar dependencias:

   ```bash
   pip install -r requeriment.txt
   ```

3. Configurar `DATABASE_URL` en un archivo `.env` según tu instalación de MySQL. Ejemplo:

   ```env
   DATABASE_URL=mysql+pymysql://root:tu_password_root@localhost:33061/db_kardex
   ```

4. Ejecutar:

   ```bash
   uvicorn src.main:app --reload --port 8001
   ```

5. Abrir http://localhost:8001/.

## Perfiles incluidos en la interfaz

- Cliente / Usuario de consulta: consulta el catálogo de lotes y movimientos.
- Trabajador de finca: registra cosechas y consulta lotes.
- Encargado / Jefe: administra fincas, parcelas, cosecheros, lotes y movimientos.

La aplicación reutiliza los endpoints y tablas existentes. En el modelo actual, el catálogo de productos se representa mediante la tabla `lotes`; no se ha agregado una tabla independiente de productos ni un módulo de ventas/pedidos.

## Importante antes de producción

Esta entrega está preparada como prototipo académico para demostración. El backend original no implementa autorización por token ni permisos por rol en los endpoints. La selección de perfil en el registro permite mostrar las distintas interfaces, pero NO es una barrera de seguridad: una persona podría solicitar directamente endpoints de escritura. Además, el registro público permite seleccionar el rol de encargado y el esquema inicial MySQL define los roles `admin`, `operador` y `consulta`.

Antes de usar con datos reales:
- restringir el alta de cuentas `admin` a un administrador autorizado;
- implementar autenticación con sesión/JWT y autorización en cada endpoint;
- sustituir SHA-256 simple por Argon2id o bcrypt para contraseñas;
- validar existencias y movimientos por lote dentro de transacciones;
- configurar contraseñas seguras mediante variables de entorno;
- realizar copias de seguridad de MySQL.

## Cambios incluidos

- Interfaz de inicio de sesión y registro.
- Tres vistas según perfil.
- Panel de resumen con indicadores.
- Catálogo de lotes / productos.
- Formularios para cosechas, movimientos, cosecheros, fincas y parcelas.
- Integración con endpoints FastAPI existentes.
- Corrección de la ubicación de las entidades `Cosecha` y `Movimiento` en `domain/models.py`, manteniendo imports antiguos compatibles.
- Ruta raíz `/` para mostrar la interfaz y `/health` para comprobar el servicio.
