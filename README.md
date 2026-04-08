# Alke Wallet

Aplicacion web desarrollada con Django para gestionar clientes y operaciones financieras basicas usando SQLite y el ORM de Django.

## Requisitos
- Python 3.11 o superior
- Entorno virtual local en `.venv`

## Instalacion y ejecucion

```bash
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py runserver
```

## Datos de ejemplo

Para cargar clientes y transacciones de demostracion:

```bash
./.venv/bin/python manage.py seed_demo_data
```

## Modelo de datos

### Customer
- Nombre y apellido
- Correo electronico unico
- Telefono
- Saldo acumulado
- Fechas de creacion y actualizacion

### Transaction
- Cliente asociado mediante `ForeignKey`
- Tipo de operacion: deposito, retiro o transferencia
- Monto
- Descripcion opcional
- Fechas de creacion y actualizacion

La relacion entre modelos es de uno a muchos: un cliente puede tener multiples transacciones.

## Funcionalidades
- CRUD completo de clientes
- CRUD completo de transacciones
- Actualizacion automatica del saldo del cliente
- Validacion para evitar retiros o transferencias sin saldo suficiente
- Panel principal con resumen de clientes, transacciones y saldo total
- Integracion con el panel de administracion de Django

## Rutas principales
- `/` panel principal
- `/customers/` gestion de clientes
- `/transactions/` gestion de transacciones
- `/admin/` panel de administracion

## Base de datos y migraciones
El proyecto usa SQLite como base de datos local en `db.sqlite3`.

Comandos principales:

```bash
./.venv/bin/python manage.py makemigrations wallet
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py test
./.venv/bin/python manage.py check
```

## Documentacion adicional
- `DOCUMENTACION.md`: explicacion del modelo de datos, reglas de negocio, CRUD y validaciones

## Entregable
Este proyecto cubre:
- Definicion de modelos con ORM
- Relacion simple entre modelos
- Migraciones sincronizadas con el esquema
- Operaciones CRUD integradas con vistas y templates
- Persistencia de datos con SQLite
