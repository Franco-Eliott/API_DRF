from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from shop.views import CategoryViewset, ProductViewset

# nous creons le routeur
router = routers.SimpleRouter()
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
