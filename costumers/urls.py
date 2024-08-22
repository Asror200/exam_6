from django.urls import path
from costumers import views
from django.conf.urls.i18n import set_language
urlpatterns = [

    path('customers', views.CustomerListView.as_view(), name='home'),
    path('customer-detail/<slug:_slug>/', views.CustomerDetailView.as_view(), name='customer_details'),
    path('calendar-page/', views.CalendarView.as_view(), name='calendar'),
    path('shopping-cart/', views.ShoppingCartListView.as_view(), name='shopping_cart'),
    path('i18n/setlang/', set_language, name='set_language'),
    path('sending-email/', views.SendingEmail.as_view(), name='sending-email'),

    # action over customers
    path('add-customer/', views.CustomerCreateView.as_view(), name='add_customer'),
    path('edite-customer/<slug:_slug>/', views.CustomerUpdateView.as_view(), name='edit_customer'),
    path('delete-customer/<slug:_slug>/', views.CustomerDeleteView.as_view(), name='delete_customer'),


]