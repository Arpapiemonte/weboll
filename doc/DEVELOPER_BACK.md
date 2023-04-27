# weboll - Back-end Developer Guide

The back-end is implemented in the Python 3.9 language with the [Django web framework](https://www.djangoproject.com/).

It is an "API only" Django project based on [Django REST framework (DRF)](https://www.django-rest-framework.org/); there are no app forms/visual interfaces except the admin interface, the API playground provided by DRF:

- http://localhost:8000/w05/

- http://localhost:8000/w16/

- ...

and the API docs provided by [drf-spectacular](https://github.com/tfranzel/drf-spectacular):

- interactive API documentation: [http://localhost:8000/docs/](http://localhost:8000/docs/)

- [OpenApi3 ("swagger") schema](https://www.openapis.org/) in JSON format: http://localhost:8000/schema/?format=json&lang=it

Two authentication mechanisms are supported:

- sessionless: with [JSON Web Tokens (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token) provided by 
[Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)
  - to keep it simple, we are not using the refresh token: the access tokens are long-lived
  - ideally we'd like to secure the API with a JWT sent as a http-only, secure and `same-site=strict` cookie, but that is not yet supported, see this PR: https://github.com/SimpleJWT/django-rest-framework-simplejwt/pull/157
- with server session saved to database, required for the Django visual admin interface

There are also two authentication backends:

- Django's own user/group models, for the emergency non-LDAP users
- LDAP bridge with Active Directory.

All Python code follows the [Black code style](https://github.com/ambv/black), the PEP8 Style Guide as per [flake8](https://github.com/pycqa/flake8), and import ordering as per [isort](https://github.com/PyCQA/isort).

The project was initialy generated with [Cookiecutter Django](https://github.com/pydanny/cookiecutter-django/) but is now manually managed.

## Settings

See the [Cookiecutter Django settings reference](http://cookiecutter-django.readthedocs.io/en/latest/settings.html)

## Starting the service

If you run with docker, the service starts automatically.

If you work locally start the back-end service with:
```
env $(<.env) ./compose/backend/start
```

## Populating the database with test data

A database dump for testing purposes is available in [/sql/*.sql].

It is automatically loaded into the database when the app is run in local development mode with docker; you can update w05 bulletin data with this command:

    cat sql/024_load_w05.sql | docker-compose exec -T postgres psql -U weboll core

If you work locally you must run this manually to populate the database:

    cat sql/*.sql | env -i $(<.env) sh -c 'psql -U $POSTGRES_USER $POSTGRES_DB -f -'

To populate the test database `test_hello`:

    cat sql/* | docker-compose exec -T postgres psql -U REPLACE_ME test_hello

## Setting Up Users

If you run the back-end with the docker set-up, it authenticates users against a mock LDAP server, with three pre-defined users: `aliccoop` ,`billidol` and `carlbrun`, all with password: `mypass`.

To create a **superuser account**, launch this command [inside the django service](https://docs.docker.com/compose/reference/exec/):

    docker-compose exec django python3 manage.py createsuperuser

of if you work locally use:

    env $(<.env) ./manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

## Manually inspect the API

Open the Django REST framework Api Root: [http://localhost:8000](http://localhost:8000)

Open the Django administration Site: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Inspect the database

### Docker set-up

    docker-compose exec postgres psql -U weboll core -c '\l'
    docker-compose exec postgres psql -U weboll core -c '\dt'
    ...
    (11 rows)

    docker-compose exec postgres psql -U weboll core -c 'SELECT schemaname,relname,n_live_tup FROM pg_stat_user_tables WHERE n_live_tup > 0 ORDER BY n_live_tup DESC'
    schemaname |       relname       | n_live_tup 
    ------------+---------------------+------------
    public     | auth_permission     |         28
    public     | django_migrations   |         19
    public     | django_content_type |          7
    public     | auth_user           |          1
    public     | django_session      |          1
    public     | django_site         |          1
    (6 rows)

    docker-compose exec postgres psql -U weboll core -c 'select * from auth_user'
    id |                                 password                                  |          last_login             | is_superuser | username | first_name | last_name |     email      | is_staff | is_active |            date_joined          
    ---+---------------------------------------------------------------------------+---------------------------------+--------------+----------+------------+-----------+----------------+----------+-----------+------------------------------
    1  | argon2$argon2i$v=19$m=512,t=2,p=2$SzJaQm5YM0ROdDNi$LQK+XfY2fFp3KS/pfgT+3Q | 2020-12-22 09:03:00.005679+00   | t            | root     |            |           | root@localhost | t        | t         | 2020-12-22 09:02:53.03557+00
    (1 row)

### Local set-up

Clear database (optional):
```
env -i $(<.env) sudo -E -u postgres sh -c 'dropdb $POSTGRES_DB'
```

Create database, set owner and rights:
```
env -i $(<.env) sudo -E -u postgres sh -c 'createdb -O $POSTGRES_USER $POSTGRES_DB'
env -i $(<.env) sudo -E -u postgres sh -c 'psql -c "GRANT pg_execute_server_program TO $POSTGRES_USER"'
```

Inspect the database:
```
env -i $(<.env) sh -c 'psql -U $POSTGRES_USER $POSTGRES_DB'
```

**NOTE**: All this assumes [Peer Authentication](https://www.postgresql.org/docs/current/auth-peer.html) is set in `/etc/postgresql/13/main/pg_hba.conf` for local connections:
```
local   all             all                                     peer
```
