from django.urls import path
from app import views

urlpatterns = [
    path('', views.BookView.as_view(), name='index'),
]