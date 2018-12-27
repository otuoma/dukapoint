from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create-product/', views.CreateProduct.as_view(), name='create-product'),
    path('update-product/<int:pk>/', views.UpdateProduct.as_view(), name='update-product'),
    path('delete-product/<int:pk>/', views.DeleteProduct.as_view(), name='delete-product'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),

]
