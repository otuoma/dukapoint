from django.urls import path
from branches import views

app_name = 'branches'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create-branch/', views.CreateBranch.as_view(), name='create-branch'),
    path('update-branch/<int:pk>/', views.UpdateBranch.as_view(), name='update-branch'),
    path('delete-branch/<int:pk>', views.DeleteBranch.as_view(), name='delete-branch'),

]
