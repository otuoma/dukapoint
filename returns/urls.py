from django.urls import path
from returns import views

app_name = 'returns'

urlpatterns = [
    path('', views.ViewReturns.as_view(), name='home'),
    path('add-return/', views.AddReturn.as_view(), name='add-return'),
    path('search-product/', views.SearchProduct.as_view(), name='search-product'),
]

