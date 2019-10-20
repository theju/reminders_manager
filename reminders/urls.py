from django.urls import path, re_path

from .views import ReminderCreateView, ReminderUpdateView, ReminderDeleteView, \
    ReminderListView, RegisterView, RobotsTxtView, ReminderReadOnlyView

urlpatterns = [
    re_path('robots.txt$', RobotsTxtView.as_view(), name="robots_view"),
    path('signup/', RegisterView.as_view(), name="signup"),

    path('reminder/add/', ReminderCreateView.as_view(), name="reminder_add"),
    re_path('reminder/view/(?P<uuid>[\w\-]+)/', ReminderReadOnlyView.as_view(), name="reminder_view"),
    re_path('reminder/edit/(?P<pk>\d+)/', ReminderUpdateView.as_view(), name="reminder_edit"),
    re_path('reminder/delete/(?P<pk>\d+)/', ReminderDeleteView.as_view(), name="reminder_delete"),
    path('reminders/', ReminderListView.as_view(), name="reminders_list"),
]
