from django.urls import path
from .views import jobs, register,applications, notifications
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("jobs/", jobs, name="jobs"),
    path("register/", register, name="register"),
    path("applications/", applications, name="applications"),
    path("notifications/", notifications, name="notifications"),
]
