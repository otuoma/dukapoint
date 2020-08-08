"""dukapoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dukapoint import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('suppliers/', include('suppliers.urls', namespace='suppliers')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('staff/', include('staff.urls', namespace='staff')),
    path('products/', include('products.urls', namespace='products')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('branches/', include('branches.urls', namespace='branches')),
    path('deliveries/', include('deliveries.urls', namespace='deliveries')),
    path('returns/', include('returns.urls', namespace='returns')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
