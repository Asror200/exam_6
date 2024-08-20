from django.urls import path
from user import views

urlpatterns = [
# authentication users
    path('register-page/', views.register_user, name='register_page'),
    path('login-page/', views.login_user, name='login_page'),
    path('logout-page/', views.logout_user, name='logout_page'),
    path('forgotten-password/', views.forgot_password, name='forgotten_password'),
              ]