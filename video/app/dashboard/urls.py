# coding:utf-8

from django.urls import path
from .views.base import Index
from .views.auth import Login

urlpatterns = [
    path('',Index.as_view()),
    path('login',Login.as_view(),name='dashboard_login')
]