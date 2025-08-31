from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Branch, Warehouse, Vendor, Customer, Seller, WarehouseTransaction
from .serializers import (
    BranchSerializer, WarehouseSerializer, VendorSerializer, 
    CustomerSerializer, SellerSerializer, WarehouseTransactionSerializer
)
from utils.permissions import IsAdminOrManager, SameBranchPermission

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_date']
    search_fields = ['name']
    ordering_fields = ['name', 'created_date']
    ordering = ['-created_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        branch = self.get_object()
        branch.restore()
        return Response({'message': 'Branch restored successfully'})

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['branch', 'created_date']
    search_fields = ['code', 'branch__name']
    ordering_fields = ['code', 'cash', 'created_date']
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(branch=self.request.user.branch)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        warehouse = self.get_object()
        warehouse.restore()
        return Response({'message': 'Warehouse restored successfully'})

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_date']
    search_fields = ['name']
    ordering_fields = ['name', 'created_date']
    ordering = ['-created_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        vendor = self.get_object()
        vendor.restore()
        return Response({'message': 'Vendor restored successfully'})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_date']
    search_fields = ['name', 'phone']
    ordering_fields = ['name', 'phone', 'created_date']
    ordering = ['-created_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        customer = self.get_object()
        customer.restore()
        return Response({'message': 'Customer restored successfully'})

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['branch', 'created_date']
    search_fields = ['name', 'branch__name']
    ordering_fields = ['name', 'created_date']
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            queryset = queryset.filter(branch=self.request.user.branch)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        seller = self.get_object()
        seller.restore()
        return Response({'message': 'Seller restored successfully'})

class WarehouseTransactionViewSet(viewsets.ModelViewSet):
    queryset = WarehouseTransaction.objects.all()
    serializer_class = WarehouseTransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'from_warehouse', 'to_warehouse', 'created_date']
    search_fields = ['item_name', 'from_warehouse__code', 'to_warehouse__code']
    ordering_fields = ['item_name', 'quantity', 'status', 'created_date', 'action_date']
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's branch if not admin
        if self.request.user.role != 'Admin':
            user_branch = self.request.user.branch
            queryset = queryset.filter(
                models.Q(from_warehouse__branch=user_branch) | 
                models.Q(to_warehouse__branch=user_branch)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            action_by=self.request.user,
            action_date=timezone.now()
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status != 'Pending':
            return Response(
                {'error': 'Only pending transactions can be approved'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = 'Approved'
        transaction.action_by = request.user
        transaction.action_date = timezone.now()
        transaction.save()
        
        return Response({'message': 'Transaction approved successfully'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status != 'Pending':
            return Response(
                {'error': 'Only pending transactions can be rejected'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = 'Rejected'
        transaction.action_by = request.user
        transaction.action_date = timezone.now()
        transaction.save()
        
        return Response({'message': 'Transaction rejected successfully'})