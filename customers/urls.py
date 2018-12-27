from django.urls import path
from customers import views

app_name = 'customers'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add-new/', views.CreateCustomer.as_view(), name='create-customer'),
    path('update-customer/<int:pk>', views.UpdateCustomer.as_view(), name='update-customer'),
    path('delete-customer/<int:pk>', views.DeleteCustomer.as_view(), name='delete-customer'),
]

