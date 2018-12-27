from django.urls import path
from suppliers import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add-new/', views.CreateSupplier.as_view(), name='create-supplier'),
    path('update-supplier/<int:pk>', views.UpdateSupplier.as_view(), name='update-supplier'),
    path('delete-supplier/<int:pk>', views.DeleteSupplier.as_view(), name='delete-supplier'),
]

