# !/bin/bash
echo ">>> first_time_setup initialization"
echo "creating new db..."
createdb --username=mattjaikaran django_boilerplate_db # change username
echo "db created"

echo "Updating Pip"
pip install --upgrade pip
echo "Pip updated"

echo "Creating virtual environment"
python3 -m venv env
echo "Virtual environment created"

echo "Activating virtual environment"
source env/bin/activate
echo "Virtual environment activated"


echo "Installing requirements"
pip install -r requirements.txt
echo "Requirements installed"

cat .env.example >> .env.local
python3 manage.py collectstatic
python3 manage.py migrate
python3 manage.py create_superuser # creates superuser based on env file data

python3 manage.py loaddata core/seed/users.json --app core --format=json # example seed data (data from jsonplaceholder)

echo ">>> Generating new secret key"
python3 manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()); exit()" | pbcopy
echo "Secret key copied to clipboard"

echo ">>> first_time_setup complete"
echo ">>> Paste the secret in your .env file"

# echo ">>> Running server"
# python3 manage.py runserver

# # python3 manage.py loaddata projects/seed/categories.json --app projects --format=json # example seed data
# example - 
# # python3 manage.py loaddata {APP_NAME}/seed/categories.json --app {APP_NAME} --format=json # example seed data