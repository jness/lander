# Lander

[![workflow](https://github.com/jness/lander/actions/workflows/main.yml/badge.svg)](https://github.com/jness/lander/actions/workflows/main.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.5-blue.svg)](https://www.djangoproject.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Django application for dynamically hosting multiple landing pages,
and scheduling management commands using cron.

![logo](docs/images/logo.jpg)

> Disclaimer: The cron scheduling logic is not scaleable across
> multiple web instances. something like Celery may work for that.

## Images

![landing](docs/images/landing.jpg)
![admin](docs/images/admin.jpg)
![api](docs/images/api.jpg)

## Demo

[![video](https://img.youtube.com/vi/JA59_q2SHTg/0.jpg)](https://www.youtube.com/watch?v=JA59_q2SHTg)

## Development (local)

### Install with container environment

Lander is capable of running in many different runtimes,
feel free to use which ever works best for you.

* https://docs.docker.com/get-docker/
* https://podman.io/

### Configuration

Lander ships with a working dev configuration, found at `project/settings.py`.

Overrides and/or production configuration can be added to a non git tracked
`project/settings_local.py` file, if present this configuration is loaded
from the bottom of the shipped project/settings.py.

### Startup

Using the `{runtime}-launch.sh` script for your container enviornment, build and start your application:

> Use docker-lauch.sh for Docker, and podman-launch.sh for Podman.

```
./{runtime}-launch.sh build
./{runtime}-launch.sh start
```

### Initialize

On first run your database will need to run schema migrations, as well as creating the administrator user.

```
$ ./{runtime}-launch.sh init
```

### Stopping

To stop your containers use your `{runtime}-launch.sh` script:

```
$ ./{runtime}-launch.sh stop
```

### Create One Time Password (OTP)

If `OTP_ENABLED` is set to **True** in `settings.py` you will need to setup a TOTP device, scan the QR code with which ever authenticator app you like (something like Google Authenticator):

```
$ ./{runtime}-launch.sh execute ./manage.py create_totp 1
```

### Access

The initial data sets the **Primary Site** to domain `django-tacos.com`,
a secondary site also exists under `django-burgers.com`.

In order to utilize the initial domains you will need to update
your **/etc/hosts** to resolve them locally.

> Only the Primary Site routes the web admin and api.

```
$ cat /etc/hosts
127.0.0.1 django-tacos.com
127.0.0.1 django-burgers.com
```

* [http://django-tacos.com:8000](http://django-tacos.com:8000)
* [http://django-tacos.com:8000/admin/](http://django-tacos.com:8000/admin/)
* [http://django-tacos.com:8000/api/](http://django-tacos.com:8000/api)

### API token

From the admin iterface generate a new **Authtoken.Token** for the user:

* [http://django-tacos.com:8000/admin/authtoken/tokenproxy/](http://django-tacos.com:8000/admin/authtoken/tokenproxy/)

> This key allows read/write access to your models, keep it secret!

```
$ curl -sLH 'Authorization: Token 42abc.................' http://django-tacos.com:8000/api/sites
[
    {
        "url": "http://django-tacos.com:8000/api/sites/2/",
        "domain": "django-burgers.com",
        "name": "django-burgers"
    },
    {
        "url": "http://django-tacos.com:8000/api/sites/1/",
        "domain": "django-tacos.com",
        "name": "django-tacos"
    }
]
```

### Application access

```
./{runtime}-launch.sh execute ./manage.py shell

Python 3.12.0 (main, Oct 12 2023, 00:42:11) [GCC 12.2.0] on linux
>>>
>>> from app.models import Template
>>> Template.objects.get(id=1)
<Template: one_page_wonder>
```

### Database access

```
$  ./{runtime}-launch.sh execute ./manage.py dbshell
```

Once connected a familiar sqlite shell is shown:

```
sqlite> .tables
app_article                   auth_user_groups
app_contact                   auth_user_user_permissions
app_landing                   authtoken_token
app_price                     django_admin_log
app_schedule                  django_content_type
app_schedulelog               django_migrations
app_template                  django_session
app_testimonial               django_site
auth_group                    django_summernote_attachment
auth_group_permissions        otp_static_staticdevice
auth_permission               otp_static_statictoken
auth_user                     otp_totp_totpdevice
```

```
sqlite> SELECT * FROM django_site;
1|django-tacos|django-tacos.com
2|django-burgers|django-burgers.com
```

### Schedules

Lander is capable of using an existing cron daemon (setup separately) to schedule
management commands, merely enable `CRON_SCHEDULES` in **project/settings.py**.

In order to allow the application to write `/etc/cron.d/` files
in production, one solution is to utilize **sudo**, set `CRON_SCHEDULES_WITH_SUDO` to **True**.

```
$ visudo
...
django ALL=NOPASSWD: /usr/bin/tee /etc/cron.d/django_*
django ALL=NOPASSWD: /usr/bin/rm -rf /etc/cron.d/django_*
...
```

### Test Cases

Django’s unit tests uses the Python standard library module `unittest`.

Lander's test cases are located in `app/tests.py`.

To run tests simply leverage **manage.py** test subcommand:

```
$ ./{runtime}-launch.sh execute ./manage.py test

Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.026s

OK
Destroying test database for alias 'default'...
```

Since Django uses Python's standard library unittest, we can also leverage
the Python's 3rd party package `coverage`.

```
$ ./{runtime}-launch.sh execute pip install coverage
```

Once installed re-run your test using **coverage**:

```
$ ./{runtime}-launch.sh execute coverage run --source='.' manage.py test
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.081s

OK
Destroying test database for alias 'default'...
```

Then use the coverage `report` sub-command to view the results:

```
$ ./{runtime}-launch.sh execute coverage report
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
app/__init__.py                           0      0   100%
app/admin.py                             87      3    97%
app/api.py                               48      0   100%
app/apps.py                               4      0   100%
app/authentication_backends.py           14     14     0%
app/context_processors.py                 5      0   100%
app/forms.py                              6      0   100%
app/middleware.py                        24      7    71%
app/migrations/0001_initial.py           10      0   100%
app/migrations/0002_price_link.py         4      0   100%
app/migrations/0003_landing_link.py       4      0   100%
app/migrations/__init__.py                0      0   100%
app/models.py                           173     41    76%
app/serializers.py                       55      0   100%
app/tests.py                             28      0   100%
app/urls.py                              21      0   100%
app/views.py                             28     14    50%
manage.py                                11      2    82%
project/__init__.py                       0      0   100%
project/asgi.py                           4      4     0%
project/settings.py                      44      5    89%
project/settings_local.py                 0      0   100%
project/urls.py                           2      0   100%
project/wsgi.py                           4      4     0%
---------------------------------------------------------
TOTAL                                   576     94    84%
```
