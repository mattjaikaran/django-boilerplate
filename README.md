# Matt Django Boilerplate

My Django DRF REST API Starter with all that cool config stuff I like and need to get started.

Newest DRF, Postgres, Railway config. Easily hook a front end into.

### Features

- Users
  - Organization/Team config commented out
- Mailer (WIP)
- Notifications feature
- Messaging feature
  - ie Inbox with messages
- Pagination
<!-- - Stripe payment processor (WIP) -->
- Swagger docs

### Technologies

- Python 3.11.2
- Django 4.2
- Django Rest Framework 3.14
- Postgres 14
- [Django Rest Framework SimpleJWT Auth](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
  - Session Auth
  - Access Token
  - Refresh Token
  - Token Blacklist
- [Unfold Admin Panel](https://github.com/unfoldadmin/django-unfold)
- Bash and Python scripts
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
- Django Storages for S3
  - Hosts static files (ie - admin panel, images)
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
$ python3 -m venv env # using the venv virtual environment
$ source env/bin/activate # activate the environment
$ git clone URL
$ cd REPO_NAME
$ touch .env # create a new env file
# update the .env file with necessary values -> db info, superuser info
$ pip3 install -r requirements.txt # install dependencies from requirements.txt
$ python3 manage.py migrate # apply migration files to your local db
$ python3 manage.py create_superuser # runs custom script to create a superuser
$ ./scripts/generate_secret_key.sh # generate new secret key
$ python3 manage.py runserver # run the local server on http://localhost:8000
```

### Generate a new Django Secret Key

Can run `./scripts/generate_secret_key.sh`

```bash
$ python3 manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# copy generated code and paste value as SECRET_KEY variable in .env file
>>> exit()
```

## DX Tools

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
$ createdb --username=USERNAME my_db # create db
$ dropdb my_db # drop db
$ psql my_db # enter shell if necessary
```
