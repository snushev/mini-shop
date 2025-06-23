from . import models
from . import serializers
from .permissions import IsOwner
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'sku', 'category']
    search_fields = ['name','sku', 'category__name']
    ordering_fields = ['created_at', 'updated_at', 'name', 'price']
    ordering = ['created_at']

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(owner=self.request.user)


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['created_at']

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    def get_queryset(self):
        return models.Customer.objects.filter(owner=self.request.user)

class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['created_at']

    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer

    def get_queryset(self):
        return models.Supplier.objects.filter(owner=self.request.user)


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'supplier', 'purchase_date']
    search_fields = ['product__name', 'supplier__name', 'purchase_date']
    ordering_fields = ['created_at', 'updated_at', 'purchase_date', 'price']
    ordering = ['created_at']

    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    def get_queryset(self):
        return models.Purchase.objects.filter(owner=self.request.user)

class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'customer']
    search_fields = ['product__name', 'customer__name']
    ordering_fields = ['created_at', 'updated_at', 'price']
    ordering = ['created_at']

    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer

    def get_queryset(self):
        return models.Sale.objects.filter(owner=self.request.user)

class RegisterView(CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.RegisterSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

