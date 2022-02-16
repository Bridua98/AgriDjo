#!/bin/bash
python manage.py migrate
python manage.py loaddata initial_pais_data.json
python manage.py loaddata initial_departamento_data.json
python manage.py loaddata initial_distrito_data.json
python manage.py loaddata initial_localidad_data.json
python manage.py loaddata initial_tipoItem_data.json
