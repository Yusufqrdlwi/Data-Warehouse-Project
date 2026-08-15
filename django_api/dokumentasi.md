# Set Up Virtual Environtment
python3 -m venv env
source env/bin/activate

pip install django djangorestframework 

# Membuat project bernama 'core' (tanda titik artinya di folder saat ini)
django-admin startproject core .

## Membuat app bernama 'api'
python manage.py startapp api

# Menjalankan django api di laptop agar bisa diakses laptop lain melalui wifi
python manage.py runserver 0.0.0.0:8000