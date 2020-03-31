import datetime

from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.template import loader
from django.template import Context
from django.core.mail import send_mass_mail
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from reminders.models import Reminder


class Command(BaseCommand):
    help = 'Send Reminders for T-30, T-14, T-7, T-1 and T-0 days'

    def handle(self, *args, **kwargs):
        today = timezone.now().today().date()

        t_30 = today + datetime.timedelta(days=30)
        t_14 = today + datetime.timedelta(days=14)
        t_7 = today + datetime.timedelta(days=7)
        t_1 = today + datetime.timedelta(days=1)
        t_0 = today + datetime.timedelta(days=0)

        qs = Reminder.objects.filter(
            Q(reminder__date=t_30)|
            Q(reminder__date=t_14)|
            Q(reminder__date=t_7)|
            Q(reminder__date=t_1)|
            Q(reminder__date=t_0)
        )
        outputs = []
        from_email = settings.DEFAULT_FROM_EMAIL
        subject_tmpl = loader.get_template("email/reminder_subject.html")
        message_tmpl = loader.get_template("email/reminder_message.html")
        for reminder in qs:
            ctx = Context({
                "site": Site.objects.get_current(),
                "reminder": reminder
            })
            subject = subject_tmpl.render(ctx)
            message = message_tmpl.render(ctx)

            outputs.append((
                subject,
                message,
                from_email,
                [reminder.user.email]
            ))

        # Send Emails
        send_mass_mail(outputs)
        # TODO: Send Text Notification
