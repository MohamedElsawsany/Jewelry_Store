from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count
from .models import GoldProduct, SilverProduct, GoldWarehouseStock, SilverWarehouseStock
from .serializers import (
    GoldProductSerializer, SilverProductSerializer, 
    GoldWarehouseStockSerializer, SilverWarehouseStockSerializer,
    GoldStockSummarySerializer, SilverStockSummarySerializer
)
from utils.permissions import IsAdminOrManager

class GoldProductViewSet(viewsets.ModelViewSet):
    queryset = GoldProduct.objects.all()
    serializer_class = GoldProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vendor', 'carat', 'created_date']
    search_fields = ['name', 'vendor__name']
    ordering_fields = ['name', 'weight', 'carat', 'created_date']
    ordering = ['-created_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        product = self.get_object()
        product.restore()
        return Response({'message': 'Gold product restored successfully'})

class SilverProductViewSet(viewsets.ModelViewSet):
    queryset = SilverProduct.objects.all()
    serializer_class = SilverProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vendor', 'carat', 'created_date']
    search_fields = ['name', 'vendor__name']
    ordering_fields = ['name', 'weight', 'carat', 'created_date']
    ordering = ['-created_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        product = self.get_object()
        product.restore()
        return Response({'message': 'Silver product restored successfully'})

class GoldWarehouseStockViewSet(viewsets.ModelViewSet):
    queryset = GoldWarehouseStock.objects.all()
    serializer_class = GoldWarehouseStockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse', 'product', 'warehouse__branch', 'created_date']
    search_fields = ['product__name', 'warehouse__code', 'warehouse__branch__name']
    ordering_fields = ['quantity', 'created_date']
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(warehouse__branch=self.request.user.branch)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get gold stock summary by warehouse"""
        queryset = self.get_queryset()
        
        summary = queryset.values(
            'warehouse__id',
            'warehouse__code',
            'warehouse__branch__name'
        ).annotate(
            total_products=Count('product', distinct=True),
            total_quantity=Sum('quantity'),
            total_weight=Sum('product__weight')
        ).order_by('-total_quantity')
        
        # Format the response
        formatted_summary = []
        for item in summary:
            formatted_summary.append({
                'warehouse': item['warehouse__branch__name'],
                'warehouse_code': item['warehouse__code'],
                'total_products': item['total_products'],
                'total_quantity': item['total_quantity'],
                'total_weight': item['total_weight'] or 0
            })
        
        serializer = GoldStockSummarySerializer(formatted_summary, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        stock = self.get_object()
        stock.restore()
        return Response({'message': 'Gold stock restored successfully'})

    @action(detail=True, methods=['post'])
    def adjust_quantity(self, request, pk=None):
        """Adjust stock quantity"""
        stock = self.get_object()
        adjustment = request.data.get('adjustment', 0)
        
        try:
            adjustment = int(adjustment)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid adjustment value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_quantity = stock.quantity + adjustment
        if new_quantity < 0:
            return Response(
                {'error': 'Insufficient stock'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stock.quantity = new_quantity
        stock.save()
        
        return Response({
            'message': 'Stock quantity adjusted successfully',
            'new_quantity': new_quantity
        })

class SilverWarehouseStockViewSet(viewsets.ModelViewSet):
    queryset = SilverWarehouseStock.objects.all()
    serializer_class = SilverWarehouseStockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse', 'product', 'warehouse__branch', 'created_date']
    search_fields = ['product__name', 'warehouse__code', 'warehouse__branch__name']
    ordering_fields = ['quantity', 'created_date']
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(warehouse__branch=self.request.user.branch)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get silver stock summary by warehouse"""
        queryset = self.get_queryset()
        
        summary = queryset.values(
            'warehouse__id',
            'warehouse__code',
            'warehouse__branch__name'
        ).annotate(
            total_products=Count('product', distinct=True),
            total_quantity=Sum('quantity'),
            total_weight=Sum('product__weight')
        ).order_by('-total_quantity')
        
        # Format the response
        formatted_summary = []
        for item in summary:
            formatted_summary.append({
                'warehouse': item['warehouse__branch__name'],
                'warehouse_code': item['warehouse__code'],
                'total_products': item['total_products'],
                'total_quantity': item['total_quantity'],
                'total_weight': item['total_weight'] or 0
            })
        
        serializer = SilverStockSummarySerializer(formatted_summary, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        stock = self.get_object()
        stock.restore()
        return Response({'message': 'Silver stock restored successfully'})

    @action(detail=True, methods=['post'])
    def adjust_quantity(self, request, pk=None):
        """Adjust stock quantity"""
        stock = self.get_object()
        adjustment = request.data.get('adjustment', 0)
        
        try:
            adjustment = int(adjustment)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid adjustment value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_quantity = stock.quantity + adjustment
        if new_quantity < 0:
            return Response(
                {'error': 'Insufficient stock'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stock.quantity = new_quantity
        stock.save()
        
        return Response({
            'message': 'Stock quantity adjusted successfully',
            'new_quantity': new_quantity
        })