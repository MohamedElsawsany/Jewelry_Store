from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'core'

router = DefaultRouter()
router.register(r'branches', views.BranchViewSet)
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'vendors', views.VendorViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'sellers', views.SellerViewSet)
router.register(r'warehouse-transactions', views.WarehouseTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]