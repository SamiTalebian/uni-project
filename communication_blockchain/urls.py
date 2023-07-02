"""communication_blockchain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from Auction import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-member/<int:pk>', views.add_member),
    path('get-contract/<int:contract_id>', views.get_contract),
    path('create-contract/', views.create_contract),
    path('find-winner/<int:pk>', views.find_winner),
    path('place-bid/<int:pk>/<str:user_address>', views.place_bid),
]
