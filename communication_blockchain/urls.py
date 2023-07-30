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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import SimpleRouter
from Auction import views


router = SimpleRouter()
router.register('register', views.CustomUserView)

schema_view = get_schema_view(
    openapi.Info(
        title="BLockChain",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(router.urls)),
    path('auth/current-user', views.current_user),
    path('contracts/<int:contractId>/add-member', views.add_member),
    path('contracts', views.get_contracts),
    path('contracts/<int:contractId>', views.get_contract),
    path('contracts/create', views.create_contract),
    path('contracts/<int:contractId>/find-winner', views.find_winner),
    path('contracts/<int:contractId>/place-bid/<str:userId>', views.place_bid),
    path('auth/login', views.login),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
