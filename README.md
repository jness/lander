# Lander

Django application for dynamically hosting multiple landing pages,
and scheduling management commands using cron.

![logo](docs/images/logo.jpg)

> Disclaimer: The cron scheduling logic is not scaleable across
> multiple web instances. something like Celery may work for that.

## Images

![landing](docs/images/landing.png)
![admin](docs/images/admin.png)
![api](docs/images/api.png)


## Development (local)

### Install Docker

https://docs.docker.com/get-docker/

### Startup

Using the `docker-compose.yml` start your application:

```
$ docker-compose up
```

You are able to see the containers using the `ls` command:

```
$ docker-compose ls
NAME                STATUS              CONFIG FILES
lander              running(1)          /home/user/Git/lander/docker-compose.yaml
```

### Schema migrations

On first run your database and application will need schema migrations:

>  You have 31 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, app, auth, authtoken, contenttypes, otp_static, otp_totp, sessions, sites.

You can show the migrations using the management command:

```
$ docker-compose exec web ./manage.py showmigrations
```

And when ready to run use the `migrate` command:

```
$ docker-compose exec web ./manage.py migrate
```

### Initial data

The initial_data sets the `primary site` to domain **django-tacos.com**,
a secondary site also exists under **django-burgers.com**.

Only the primary site routes the web admin and api.

```
$ docker-compose exec web ./manage.py loaddata app/fixtures/initial_data.json
```

### Create super user

Next create a super user which will have access to the web admin:

```
$ docker-compose exec web ./manage.py createsuperuser
```

 ### Create OTP

If `OTP_ENABLED` is set to **True** in `settings.py` you will need to setup a
TOTP device, scan the QR code with which ever authenticator app you are using.

```
$ docker-compose exec web ./manage.py create_totp 1
```

### Install Podman

### Startup

Using the `podman-launch.sh` start your application:

```
$ ./podman-launch.sh start
```

### Application initalization

https://podman.io/

When ready to run use the `init` command:

```
$ ./podman-launch.sh init
```

### Access

In order to utilize the initial example domains you will need to update
your **/etc/hosts**:

```
$ cat /etc/hosts
127.0.0.1 django-tacos.com
127.0.0.1 django-burgers.com
```

* [http://django-tacos.com:8000](http://django-tacos.com:8000)
* [http://django-tacos.com:8000/admin/](http://django-tacos.com:8000/admin/)
* [http://django-tacos.com:8000/api/](http://django-tacos.com:8000/api)

### API token

From the admin iterface add a new **Authtoken.Token** for the user:

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

### Database access

```
$  docker-compose exec web ./manage.py dbshell
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

Lander is capable of using an existing cron daemon to schedule
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
