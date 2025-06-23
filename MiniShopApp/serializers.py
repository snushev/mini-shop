from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField( 
        default=serializers.CurrentUserDefault()
    )
    category = serializers.SlugRelatedField(slug_field='name', queryset=models.Category.objects.all())

    class Meta:
        model = models.Product
        fields = ['name', 'sku', 'price', 'quantity_in_stock', 'owner', 'category', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CustomerSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Customer
        fields = ['name', 'email', 'phone', 'address', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['created_at', 'updated_at']

class SupplierSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = models.Supplier
        fields = ['name', 'contact_email', 'phone', 'address', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['created_at', 'updated_at']

class PurchaseSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    product = serializers.SlugRelatedField(slug_field='name', queryset=models.Product.objects.all())
    supplier = serializers.SlugRelatedField(slug_field='name', queryset=models.Supplier.objects.all())

    class Meta:
        model = models.Purchase
        fields = ['product', 'supplier', 'quantity', 'purchase_date', 'unit_cost_price', 'total_price', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['created_at', 'updated_at']
    
class SaleSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', queryset=models.Product.objects.all())
    customer = serializers.SlugRelatedField(slug_field='name', queryset=models.Customer.objects.all())
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Sale
        fields = ['product', 'quantity', 'sale_date', 'customer', 'sale_price', 'total_price', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
    
        
    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "user_id": instance.id,
            "username": instance.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }