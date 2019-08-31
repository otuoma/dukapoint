from django.urls import path
from sales import views

app_name = 'sales'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('search-products', views.SearchProducts.as_view(), name='search-products'),
    path('add-to-cart', views.AddToCart.as_view(), name='add-to-cart'),
    path('clear-cart', views.ClearCart.as_view(), name='clear-cart'),
    path('delete-from-cart/<int:product_id>/', views.DeleteCartProduct.as_view(), name='delete-from-cart'),
    path('check-out/', views.CheckOut.as_view(), name='check-out'),
    path('reports-home/', views.ReportsHome.as_view(), name='reports-home'),
]

