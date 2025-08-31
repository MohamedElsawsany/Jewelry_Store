from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from .models import GoldInvoice, GoldInvoiceItem, SilverInvoice, SilverInvoiceItem
from .serializers import (
    GoldInvoiceSerializer, GoldInvoiceCreateSerializer, GoldInvoiceItemSerializer,
    SilverInvoiceSerializer, SilverInvoiceCreateSerializer, SilverInvoiceItemSerializer,
    InvoiceSummarySerializer, DailySalesSerializer
)

class GoldInvoiceViewSet(viewsets.ModelViewSet):
    queryset = GoldInvoice.objects.all()
    serializer_class = GoldInvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['invoice_type', 'transaction_type', 'branch', 'seller', 'warehouse', 'created_date']
    search_fields = ['customer__name', 'customer__phone', 'seller__name', 'warehouse__code']
    ordering_fields = ['total_price', 'created_date']
    ordering = ['-created_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return GoldInvoiceCreateSerializer
        return GoldInvoiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(branch=self.request.user.branch)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get gold invoice summary by type and transaction method"""
        queryset = self.get_queryset()
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_date__lte=end_date)
        
        summary = queryset.values('invoice_type', 'transaction_type').annotate(
            count=Count('id'),
            total_amount=Sum('total_price')
        ).order_by('-total_amount')
        
        serializer = InvoiceSummarySerializer(summary, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        """Get daily gold sales for the last 30 days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            created_date__date__range=[start_date, end_date],
            invoice_type='Sale'
        )
        
        daily_data = queryset.annotate(
            date=TruncDate('created_date')
        ).values('date').annotate(
            total_sales=Sum('total_price')
        ).order_by('date')
        
        # Format response
        formatted_data = []
        for item in daily_data:
            formatted_data.append({
                'date': item['date'],
                'gold_sales': item['total_sales'],
                'silver_sales': 0,  # Will be filled by frontend or separate endpoint
                'total_sales': item['total_sales']
            })
        
        return Response(formatted_data)

    @action(detail=True, methods=['get'])
    def print_invoice(self, request, pk=None):
        """Get invoice data formatted for printing"""
        invoice = self.get_object()
        serializer = self.get_serializer(invoice)
        return Response({
            'invoice_data': serializer.data,
            'print_date': datetime.now().isoformat()
        })

class GoldInvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = GoldInvoiceItem.objects.all()
    serializer_class = GoldInvoiceItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['invoice', 'vendor_name', 'item_carat']
    search_fields = ['item_name', 'vendor_name']
    ordering_fields = ['item_quantity', 'item_total_price']
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(invoice__branch=self.request.user.branch)
        return queryset

class SilverInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SilverInvoice.objects.all()
    serializer_class = SilverInvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['invoice_type', 'transaction_type', 'branch', 'seller', 'warehouse', 'created_date']
    search_fields = ['customer__name', 'customer__phone', 'seller__name', 'warehouse__code']
    ordering_fields = ['total_price', 'created_date']
    ordering = ['-created_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return SilverInvoiceCreateSerializer
        return SilverInvoiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(branch=self.request.user.branch)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get silver invoice summary by type and transaction method"""
        queryset = self.get_queryset()
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_date__lte=end_date)
        
        summary = queryset.values('invoice_type', 'transaction_type').annotate(
            count=Count('id'),
            total_amount=Sum('total_price')
        ).order_by('-total_amount')
        
        serializer = InvoiceSummarySerializer(summary, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        """Get daily silver sales for the last 30 days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            created_date__date__range=[start_date, end_date],
            invoice_type='Sale'
        )
        
        daily_data = queryset.annotate(
            date=TruncDate('created_date')
        ).values('date').annotate(
            total_sales=Sum('total_price')
        ).order_by('date')
        
        # Format response
        formatted_data = []
        for item in daily_data:
            formatted_data.append({
                'date': item['date'],
                'gold_sales': 0,  # Will be filled by frontend or separate endpoint
                'silver_sales': item['total_sales'],
                'total_sales': item['total_sales']
            })
        
        return Response(formatted_data)

    @action(detail=True, methods=['get'])
    def print_invoice(self, request, pk=None):
        """Get invoice data formatted for printing"""
        invoice = self.get_object()
        serializer = self.get_serializer(invoice)
        return Response({
            'invoice_data': serializer.data,
            'print_date': datetime.now().isoformat()
        })

class SilverInvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = SilverInvoiceItem.objects.all()
    serializer_class = SilverInvoiceItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['invoice', 'vendor_name', 'item_carat']
    search_fields = ['item_name', 'vendor_name']
    ordering_fields = ['item_quantity', 'item_total_price']
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(invoice__branch=self.request.user.branch)
        return queryset