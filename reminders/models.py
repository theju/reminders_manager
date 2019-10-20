from django.db import models
from django.urls import reverse_lazy


class Reminder(models.Model):
    user     = models.ForeignKey(
        'auth.User',
        related_name='reminder_user',
        on_delete=models.CASCADE
    )
    uuid     = models.TextField()

    subject  = models.TextField()
    message  = models.TextField(blank=True, null=True)
    document = models.FileField(blank=True, null=True)
    reminder = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse_lazy("reminder_edit", kwargs={"pk": self.id})
