import datetime

from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.sites.models import Site
from django.template import Template, Context
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
        for reminder in qs:
            ctx = Context({
                "site": Site.objects.get_current(),
                "reminder": reminder
            })
            reminder.subject = Template(reminder.subject).render(ctx)
            reminder.message = Template(reminder.message).render(ctx)

            outputs.append((
                reminder.subject,
                reminder.message,
                from_email,
                [reminder.user.email]
            ))

        # Send Emails
        send_mass_mail(outputs)
        # TODO: Send Text Notification
