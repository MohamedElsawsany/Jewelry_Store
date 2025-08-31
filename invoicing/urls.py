from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'invoicing'

router = DefaultRouter()
router.register(r'gold-invoices', views.GoldInvoiceViewSet)
router.register(r'gold-invoice-items', views.GoldInvoiceItemViewSet)
router.register(r'silver-invoices', views.SilverInvoiceViewSet)
router.register(r'silver-invoice-items', views.SilverInvoiceItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]