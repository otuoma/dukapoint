from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create-product/', views.CreateProduct.as_view(), name='create-product'),
    path('update-product/<int:pk>/', views.UpdateProduct.as_view(), name='update-product'),
    path('delete-product/<int:pk>/', views.DeleteProduct.as_view(), name='delete-product'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('view-transfers/', views.ViewTransfers.as_view(), name='view-transfers'),
    path('transfer-products/', views.TransferProducts.as_view(), name='transfer-products'),
    path('view-transfer-products/<int:transfer_id>', views.ViewTransferProducts.as_view(), name='view-transfer-products'),
    path('add-product/', views.AddProduct.as_view(), name='add-product'),
    path('delete-cart-product/<int:product_id>/', views.DeleterCartProduct.as_view(), name='delete-cart-product'),
    path('clear-list/', views.ClearList.as_view(), name='clear-list'),
    path('set-transfer-to/', views.SetTransferTo.as_view(), name='set-transfer-to'),
    path('process-transfer/', views.ProcessTransfer.as_view(), name='process-transfer'),
    path('receive-transfer/<int:transfer_id>/', views.ReceiveTransfer.as_view(), name='receive-transfer'),

]
