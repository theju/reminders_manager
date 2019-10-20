import os
import uuid

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template import Template, Context
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Reminder
from .forms import ReminderForm, UserForm


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("reminders_list")

    def form_valid(self, form):
        form.instance.username = form.instance.email
        form.instance.set_password(form.instance.password)
        response = super(RegisterView, self).form_valid(form)
        login(self.request, form.instance)
        return response


class ReminderCreateView(CreateView):
    model = Reminder
    form_class = ReminderForm
    success_url = reverse_lazy("reminders_list")
    template_name = "reminders/reminder_add.html"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.uuid = str(uuid.uuid4())
            doc_file = form.instance.document
            _, file_ext = os.path.splitext(doc_file.name)
            doc_file.name = "{0}{1}".format(form.instance.uuid, file_ext)
        else:
            form.add_error("reminder", "Invalid Login")
        return super(ReminderCreateView, self).form_valid(form)


class ReminderUpdateView(UpdateView):
    model = Reminder
    form_class = ReminderForm
    template_name = "reminders/reminder_edit.html"
    success_url = reverse_lazy("reminders_list")

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Reminder.objects.filter(user=self.request.user).order_by("-reminder")
        return Reminder.objects.none()

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            doc_file = form.instance.document
            _, file_ext = os.path.splitext(doc_file.name)
            doc_file.name = "{0}{1}".format(form.instance.uuid, file_ext)
        else:
            form.add_error("reminder", "Invalid Login")
        return super(ReminderUpdateView, self).form_valid(form)


class ReminderDeleteView(DeleteView):
    model = Reminder
    success_url = reverse_lazy("reminders_list")

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Reminder.objects.filter(user=self.request.user).order_by("-reminder")
        return Reminder.objects.none()


class ReminderListView(ListView):
    model = Reminder
    paginate_by = 50

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Reminder.objects.filter(user=self.request.user).order_by("-reminder")
        return Reminder.objects.none()


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"

    def dispatch(self, request, *args, **kwargs):
        response = super(RobotsTxtView, self).dispatch(request, *args, **kwargs)
        response['Content-Type'] = "text/plain"
        return response


class ReminderReadOnlyView(DetailView):
    template_name = "reminders/reminder_view.html"
    model = Reminder

    def get_object(self):
        reminder =  Reminder.objects.get(uuid=self.kwargs.get("uuid"))
        ctx = Context({
            "reminder": reminder
        })
        reminder.subject = Template(reminder.subject).render(ctx)
        reminder.message = Template(reminder.message).render(ctx)
        return reminder
