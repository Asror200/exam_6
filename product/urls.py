from django.urls import path
from product import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product-detail/<slug:_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product-grib/', views.ProductGribView.as_view(), name='product_grib'),
    path('add-product/', views.ProductAddView.as_view(), name='product_add'),
    path('update-product/<slug:_slug>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('products/delete/<slug:slug>/', views.ProductDeleteView.as_view(), name='delete_product'),

]