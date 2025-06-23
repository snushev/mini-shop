import pytest
from MiniShopApp.models import Product, Category
from django.urls import reverse

@pytest.mark.django_db
def test_list_products(api_client, create_user):
    user = create_user(username='user1', password='password2')
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')

    product = Product.objects.create(
        name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user
    )

    response = api_client.get(reverse('product-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Laptop'


@pytest.mark.django_db
def test_create_product(api_client, create_user):
    user = create_user(username='user1', password='password2')
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name="Test")

    payload = {
        "name": "Iphone",
        "sku": "123456",
        'price': 1500,
        'quantity_in_stock': 5,
        'category': category.name
    }

    url = reverse('product-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201
    assert Product.objects.filter(name='Iphone', owner=user).exists()

@pytest.mark.django_db
def test_retrieve_product(api_client, create_user):
    user = create_user(username='test', password='password')
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Test')

    product = Product.objects.create(
        name='Dell Monitor',
        sku='MON123',
        price=300,
        quantity_in_stock=2,
        category=category,
        owner=user
    )

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == 'Dell Monitor'

@pytest.mark.django_db
def test_user_cannot_access_other_users_product(api_client, create_user):
    user = create_user(username='user1', password='pass')
    other_user = create_user(username='user2', password='pass')
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Keyboards')
    product = Product.objects.create(
        name='Gaming Keyboard',
        sku='KEY123',
        price=100,
        quantity_in_stock=1,
        category=category,
        owner=other_user
    )

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_own_product(api_client, create_user):
    user = create_user(username='user1', password='pass')
    api_client.force_authenticate(user=user)
    category = Category.objects.create(name='Tablets')

    product = Product.objects.create(
        name='Old Name',
        sku='TAB123',
        price=200,
        quantity_in_stock=1,
        category=category,
        owner=user
    )

    new_data = {
        "name": "New Name",
        "sku": "TAB123",
        "price": 250,
        "quantity_in_stock": 2,
        "category": category.name
    }
    url = reverse('product-detail', args=[product.id])
    response = api_client.put(url, new_data , format='json')

    assert response.status_code == 200
    assert product.price == 200
    product.refresh_from_db()
    assert product.name == 'New Name'
    assert product.price == 250


@pytest.mark.django_db
def test_delete_own_product(api_client, create_user):
    user = create_user(username='user1', password='pass')
    api_client.force_authenticate(user=user)
    category = Category.objects.create(name='Cameras')

    product = Product.objects.create(
        name='Camera',
        sku='CAM123',
        price=500,
        quantity_in_stock=1,
        category=category,
        owner=user
    )

    url = reverse('product-detail', args=[product.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Product.objects.filter(id=product.id).exists()

@pytest.mark.django_db
def test_Unaothorised_user_retrieve(api_client, create_user):
    user = create_user(username='test', password='password')
    category = Category.objects.create(name='Cameras')

    product = Product.objects.create(
        name='Camera',
        sku='CAM123',
        price=500,
        quantity_in_stock=1,
        category=category,
        owner=user
    )

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)

    assert response.status_code == 401