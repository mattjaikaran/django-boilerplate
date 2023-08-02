# Django Boilerplate

- Python 3.11.2
- Django 4.2
- Django Rest Framework 3.14
- Postgres DB
- Black formatter

TODO:
- Passwordless auth


# Get started

```bash
$ source env/bin/activate
$ git clone URL
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
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