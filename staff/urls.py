from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create-staff/', views.CreateStaff.as_view(), name='create-staff'),
    path('update-staff/<int:pk>/', views.UpdateStaff.as_view(), name='update-staff'),
    path('change-branch/', views.ChangeBranch.as_view(), name='change-branch'),
    path('update-password/<int:pk>/', views.UpdatePassword.as_view(), name='update-password'),
    path('set-permissions/<int:pk>/', views.SetPermissions.as_view(), name='set-permissions'),
    path('delete-staff/<int:pk>/', views.DeleteStaff.as_view(), name='delete-staff'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
