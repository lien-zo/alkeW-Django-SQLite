# Documento Explicativo - Alke Wallet

## 1. Objetivo del proyecto
Alke Wallet es una aplicacion web construida con Django para demostrar la integracion entre una aplicacion web, una base de datos relacional SQLite y el ORM de Django. El sistema permite almacenar clientes y registrar operaciones financieras basicas mediante un CRUD completo.

## 2. Tecnologias utilizadas
- Python 3.11
- Django 5.2.13
- SQLite 3
- HTML con templates de Django
- ORM de Django para persistencia y consultas

## 3. Configuracion de base de datos
La base de datos se encuentra definida en el archivo de configuracion del proyecto y utiliza SQLite con el archivo local `db.sqlite3`.

## 4. Modelo de datos
### Customer
Representa a un cliente de la billetera.
- `first_name`: nombre
- `last_name`: apellido
- `email`: correo electronico unico
- `phone`: telefono opcional
- `balance`: saldo acumulado del cliente
- `created_at`: fecha de creacion
- `updated_at`: fecha de actualizacion

### Transaction
Representa una operacion financiera asociada a un cliente.
- `customer`: relacion `ForeignKey` hacia Customer
- `transaction_type`: deposito, retiro o transferencia
- `amount`: monto de la operacion
- `description`: detalle opcional
- `created_at`: fecha de creacion
- `updated_at`: fecha de actualizacion

### Relacion entre modelos
La relacion es de uno a muchos:
- Un cliente puede tener muchas transacciones.
- Cada transaccion pertenece a un solo cliente.

## 5. Reglas de negocio implementadas
- No se permiten montos menores o iguales a cero.
- Los depositos aumentan el saldo del cliente.
- Los retiros y transferencias disminuyen el saldo del cliente.
- No se permite registrar una operacion que deje el saldo en negativo.
- Al editar o eliminar una transaccion, el saldo se recalcula automaticamente para mantener la consistencia.

## 6. Operaciones CRUD implementadas
### CRUD de clientes
- Crear cliente
- Listar clientes
- Ver detalle de cliente
- Editar cliente
- Eliminar cliente

### CRUD de transacciones
- Crear transaccion
- Listar transacciones
- Ver detalle de transaccion
- Editar transaccion
- Eliminar transaccion

## 7. Vistas y templates
Se utilizaron vistas genericas basadas en clases de Django:
- `ListView`
- `DetailView`
- `CreateView`
- `UpdateView`
- `DeleteView`
- `TemplateView`

Los templates permiten navegar por el panel principal, el listado de clientes, el listado de transacciones y los formularios para cada operacion CRUD.

## 8. Migraciones realizadas
Se ejecuto la migracion inicial de la app `wallet`, generando el archivo `0001_initial.py` y aplicandolo sobre SQLite con `migrate`.

## 9. Validacion del proyecto
Se validaron los siguientes comandos:

```bash
./.venv/bin/python manage.py makemigrations wallet
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py test
./.venv/bin/python manage.py check
```

Resultados validados:
- Migraciones generadas y aplicadas correctamente
- 6 pruebas automatizadas aprobadas
- Verificacion del proyecto sin errores mediante `check`
- Arranque correcto del servidor de desarrollo

## 10. Datos de ejemplo para demostracion
Se agrego un comando para poblar datos de muestra:

```bash
./.venv/bin/python manage.py seed_demo_data
```

Este comando crea clientes y transacciones de ejemplo para facilitar la demostracion y la toma de capturas de pantalla.

## 11. Evidencias sugeridas para la entrega
Capturas recomendadas:
- Panel principal con resumen de clientes y saldo total
- Vista de listado de clientes
- Formulario de creacion de cliente
- Vista de listado de transacciones
- Formulario de creacion de transaccion
- Panel de administracion de Django

## 12. Conclusiones
El proyecto cumple con los requerimientos del modulo al integrar Django con SQLite, definir modelos con relaciones simples, aplicar migraciones y exponer operaciones CRUD completas mediante ORM, vistas y templates.
