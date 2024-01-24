echo ">>> db_setup initialization"
# !/bin/bash

pip install --upgrade pip
python manage.py collectstatic --no-input
python3 manage.py migrate --no-input
# python3 manage.py loaddata projects/seed/categories.json --app projects --format=json # example seed data
python3 manage.py create_superuser # creates superuser based on env file data
# add custom scripts here


echo ">>> db_setup complete"