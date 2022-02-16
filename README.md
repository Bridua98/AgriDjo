# AgriDjo

```
cd invsist
python -m venv venv
cd venv\Scripts
activate
```

Crear una aplicación.
(venv) c:\invsist>python manage.py startapp inventory
Crear migraciones, cada vez que sea creado o modificado los modelos de datos.
(venv) c:\invsist>python manage.py makemigrations
Persistir migraciones en la base de datos.
(venv) c:\invsist>python manage.py migrate
Ejecutar el servidor para realizar pruebas.
(venv) c:\invsist>python manage.py runserver

## Documentación

Para agregar una nueva entrada sería necesario agregar un `.md` dentro de la carpeta `docs`

### Visualizar en desarrollo

Para actualizar la documentación es necesario ejecutar el siguiente comando:

> Crea un sitio estático compilando los `.md`

```bash
mkdocs build --clean
```

### Visualizar en producción

En Heroku la documentación es compilada en el proceso de contrucción de forma automática.


