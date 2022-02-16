#!/bin/bash
python manage.py migrate
python manage.py loaddata initial_pais_data.json
