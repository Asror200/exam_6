from django.urls import path
from user import views

urlpatterns = [
    # authentication users
    path('register-page/', views.RegisterUserView.as_view(), name='register_page'),
    path('login-page/', views.LoginUserView.as_view(), name='login_page'),
    path('logout-page/', views.LogoutUserView.as_view(), name='logout_page'),
    path('forgotten-password/', views.forgot_password, name='forgotten_password'),
    path('activation-link/<uidb64>/<token>/', views.AccountActivationView.as_view(), name='activate')

]
