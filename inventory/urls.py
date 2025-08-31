from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inventory'

router = DefaultRouter()
router.register(r'gold-products', views.GoldProductViewSet)
router.register(r'silver-products', views.SilverProductViewSet)
router.register(r'gold-stock', views.GoldWarehouseStockViewSet)
router.register(r'silver-stock', views.SilverWarehouseStockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]