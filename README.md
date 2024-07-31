# Matt Django Boilerplate

My Django REST API Starter with all that cool config stuff I like and need to get started.

Newest DRF, Postgres, Railway config. Easily hook a front end into.

### Features

- Users
  - Organization/Team config commented out
- Notifications
- Mailer
- Messaging
  - Not using websockets
- Pagination
- Stripe payment processor (WIP)
- Swagger docs

### Technologies

- Python 3.11.2
- Django 4.2
- Django Rest Framework 3.14
- Postgres 14
- Django Rest Framework [SimpleJWT Auth](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
  - Session Auth
  - Access Token
  - Refresh Token
  - Token Blacklist
- [Unfold Admin Panel](https://github.com/unfoldadmin/django-unfold)
- Bash and Python scripts (WIP)
  - Bash scripts
    - Located in `@/scripts` directory
    - `first_time_setup.sh` script (WIP)
    - `db_setup.sh` for development to quickly drop db and recreate data
  - Python scripts:
    - Can be in `@/{APP}/management/commands`
    - Superuser script
      - Creates super user based on .env file data
  - Seed data (wip)
- Data output to JSON via `serializers.py`
- Mailgun Mailer
  - Located in `@/core/emails.py`
  - In dev, emails are printed in the terminal
- Django Storages for S3 (WIP)
  - Hosts static files
- Tests via PyTest (WIP)
- Black formatter
- DRF Spectacular Swagger generator
- Railway Deployment config
  - Railway config located in `railway.json`

# Get started

<!-- **WIP**

Can run bash script located in `@/scripts/first_time_setup.sh`

What it does:

- Creates a new db
- Creates a virtual environment
- Activates the virtual env
- Installs dependencies
- Creates an .env.local and copies data from .env.example
- Creates static files
- Migrate the db
- Generates a new secret key
- Copies secret key to clipboard for you to paste into .env.local file

First Time Setup -

```bash
$ ./scripts/first_time_setup.sh
```

Or you can run the following manually - -->

```bash
$ git clone https://github.com/mattjaikaran/django-boilerplate
$ cd django-boilerplate
$ python3 -m venv env
$ source env/bin/activate
$ touch .env
$ cp .env.example .env
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
# make sure superuser data is filled out in .env
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

## DX Tools (WIP)

- `@/scripts/db_setup.sh`
  - Drops current db
  - Creates new db
  - Updates Pip
  - Run `collectstatic` command
  - Run `migration` command
  - Create superuser via `create_superuser.py` script

```bash
$ ./scripts/db_setup.sh
```

### Commands for Postgres 14

[Postgres Docs](https://www.postgresql.org/docs/14/)

```bash
$ psql my_db # enter shell
$ createdb --username=USERNAME my_db # create db
$ dropdb my_db # drop db
```
