from django.urls import path
from costumers.views import views, auth_views

urlpatterns = [

    path('', views.home, name='home'),
    path('customer-detail/<slug:_slug>/', views.customer_detail, name='customer_details'),
    path('calendar-page/', views.calendar, name='calendar'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),

    # action over customers
    path('add-customer/', views.add_customer, name='add_customer'),
    path('edite-customer/<slug:_slug>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<slug:_slug>/', views.delete_customer, name='delete_customer'),

    # authentication users
    path('register-page/', auth_views.register_user, name='register_page'),
    path('login-page/', auth_views.login_user, name='login_page'),
    path('logout-page/', auth_views.logout_user, name='logout_page'),
    path('forgotten-password/', auth_views.forgot_password, name='forgotten_password'),
]