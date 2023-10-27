echo ">> db_setup bash script"
# !/bin/bash


python3 manage.py migrate --no-input
python3 manage.py create_superuser