from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',  name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),
    path('api-token-auth/', views.obtain_auth_token),
]
