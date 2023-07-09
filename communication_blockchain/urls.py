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
router.register('users',views.CustomUserView)

schema_view = get_schema_view(
    openapi.Info(
        title="BLockChain",
        default_version='v1',
        description="APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sami9077@gmail.com"),
        license=openapi.License(name="Talebian Tazmin co."),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('add-member/<int:pk>', views.add_member),
    path('get-contract/<int:contract_id>', views.get_contract),
    path('create-contract/', views.create_contract),
    path('find-winner/<int:pk>', views.find_winner),
    path('place-bid/<int:pk>/<str:user_address>', views.place_bid),
    path('login/', views.login),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
