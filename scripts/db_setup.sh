# !/bin/bash
echo ">>> db_setup initialization"

echo ">>> db setup - running db_setup.sh"
echo "dropping django_boilerplate_db"
dropdb django_boilerplate_db
echo "db dropped"

echo "creating new db..."
createdb --username=mattjaikaran django_boilerplate_db # replace the username with yours
echo "db created"

echo "Updating Pip"
pip install --upgrade pip


echo "Creating static files..."
python manage.py collectstatic --no-input
echo "static files generated"

echo "migrating..."
python3 manage.py migrate --no-input
echo "migrate successful"

# python3 manage.py loaddata projects/seed/categories.json --app projects --format=json # example seed data
echo "creating superuser..."
python3 manage.py create_superuser # creates superuser based on env file data
echo "created superuser"

# other scripts here


echo ">>> db_setup complete"

echo ">>> Running development server..."
python3 manage.py runserver

