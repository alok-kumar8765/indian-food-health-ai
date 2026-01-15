from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('api/v1/', include('food.urls')),
    path('api/v1/', include('recipes.urls')),
    #path('api/v1/docs/', include('drf_spectacular.urls')),
]