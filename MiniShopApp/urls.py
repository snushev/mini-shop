from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'suppliers', views.SupplierViewSet, basename='supplier')
router.register(r'purchases', views.PurchaseViewSet, basename='purchase')
router.register(r'sales', views.SaleViewSet, basename='sale')


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register')
] + router.urls