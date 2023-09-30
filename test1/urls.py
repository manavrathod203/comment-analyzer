from django.urls import path
from . import views

urlpatterns = [
    path('', views.execute_script, name='execute_script'),
]
