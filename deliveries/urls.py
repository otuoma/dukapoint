from django.urls import path
from deliveries import views

app_name = 'deliveries'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('set-supplier/', views.SetSupplier.as_view(), name='set-supplier'),
    path('search-product/', views.SearchProduct.as_view(), name='search-product'),
    path('create-delivery-note/', views.CreateDeliveryNote.as_view(), name='create-delivery-note'),
    path('post-stock/', views.PostStock.as_view(), name='post-stock'),
    path('clear-delivery-note/', views.ClearDeliveryNote.as_view(), name='clear-delivery-note'),
    path('list-delivery-items/<int:delivery_id>/', views.ListDeliveryItems.as_view(), name='list-delivery-items'),
]
