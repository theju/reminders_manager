# Reminders Manager

Yet another NIH project that I have developed to send reminders to self.
Things like bill due dates, warranty reminders, birthdays etc.

It's a fairly simple system where the user first registers (`/signup/`) using
their email address and password. They next create a reminder (`/reminder/add/`)
by entering a `subject`, `message`, `document` (optional) and a `reminder` date.

The `subject` and `message` fields are rendered as django templates with the `reminder`
passed in as the context.

A total of 5 email (from the user's signup) reminders (T-30, T-14, T-7, T-1 and T-0 days)
are sent based on a script (`python manage.py send_reminders`) that is run from cron.

## INSTALL

```
$ git clone https://github.com/theju/reminders_manager.git
$ cd reminders_manager
$ pipenv shell
$ python manage.py migrate
```

## RUN THE DEV SERVER

```
$ cd reminders_manager
$ python manage.py runserver
```

## LICENSE

Licensed under the `MIT` license. Please Refer to the `LICENSE` file for more details.
