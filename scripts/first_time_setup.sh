echo ">>> first_time_setup initialization"
# !/bin/bash

# python3 -m venv env
# source env/bin/activate
# pip install -r requirements.txt
# cp .env.example .env.local
# python manage.py collectstatic --no-input
# python3 manage.py migrate --no-input
# # python3 manage.py loaddata projects/seed/categories.json --app projects --format=json # example seed data
# python3 manage.py create_superuser # creates superuser based on env file data

echo ">>> Need to do generate new secret key"
echo ">>> Entering python shell..."
# python3 manage.py shell

# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())


echo ">>> first_time_setup complete"