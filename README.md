# Django Boilerplate

Django REST Starter with all that cool stuff. WIP

### Technologies
- Python 3.11.2
- Django 4.2
- Django Rest Framework 3.14
- Postgres DB
- Black formatter
- Django Rest Framework SimpleJWT
- Authentication 
    - Access Token
    - Refresh Token
- Unfold Admin Panel
- Bash
- Railway Deployment

TODO:
- Mailer - Mailgun/Sendgrid
- Django Storage for S3


# Get started

```bash
$ git clone URL
$ cd REPO_NAME
$ python3 -m venv env
$ source env/bin/activate
$ touch .env # copy and fill out data from env.example
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py create_superuser

# before running server generate a new secret key
$ python3 manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) 
# copy generated code and paste value as SECRET_KEY variable in .env file
>>> exit()

$ python3 manage.py runserver
```

### Generate a new Django Secret Key

```bash
$ python3 manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) 
# copy generated code and paste value as SECRET_KEY variable in .env file
>>> exit()
```


### Commands for Postgres 14
[Postgres Docs](https://www.postgresql.org/docs/14/)

```bash
$ psql my_db # enter shell
$ createdb --username=USERNAME my_db # create db
$ dropdb my_db # drop db
```