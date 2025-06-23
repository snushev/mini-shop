import pytest
from MiniShopApp.models import Sale, Product, Customer, User, Category
from django.urls import reverse
from datetime import date

@pytest.mark.django_db
def test_create_sale_success(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    category = Category.objects.create(name='Electronics')
    product = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user)
    customer = Customer.objects.create(
        owner=user,
        name='Test Customer',
        email="customer@email.com",
        phone='02394943',
        address='Customer Address 25'
    )
    api_client.force_authenticate(user=user)

    payload = {
        "product": product.name,
        "customer": customer.name,
        "quantity": 5,
        "sale_date": date.today().isoformat(),
        "sale_price": "1000.00"
    }

    url = reverse("sale-list")
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201
    assert Sale.objects.filter(owner=user).count() == 1
    sale = Sale.objects.first()
    assert sale.total_price == 5000.00
    product.refresh_from_db()
    assert product.quantity_in_stock == 5

@pytest.mark.django_db
def test_sale_list_only_user(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    other = User.objects.create_user(username="user2", password="pass2")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user)
    c = Customer.objects.create(owner=other, name="Test Customer", email="t@t.bg", phone="1", address="X")
    Sale.objects.create(owner=other, product=p, customer=c, quantity=1, sale_date=date.today(), sale_price=1000.00)

    response = api_client.get(reverse("sale-list"))
    assert response.status_code == 200
    assert len(response.data["results"]) == 0

@pytest.mark.django_db
def test_get_single_sale(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user)
    c = Customer.objects.create(owner=user, name="Test Customer", email="t@t.bg", phone="1", address="X")

    sale = Sale.objects.create(owner=user, product=p, customer=c, quantity=2, sale_date=date.today(), sale_price=1000.00)

    url = reverse("sale-detail", args=[sale.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["total_price"] == "2000.00"
    assert response.data["quantity"] == 2

@pytest.mark.django_db
def test_user_cannot_access_others_sale(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    other = User.objects.create_user(username="user2", password="pass2")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user)
    c = Customer.objects.create(owner=other, name="Test Customer", email="t@t.bg", phone="1", address="X")
    sale = Sale.objects.create(owner=other, product=p, customer=c, quantity=2, sale_date=date.today(), sale_price=1000.00)

    url = reverse("sale-detail", args=[sale.id])
    response = api_client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_update_own_sale(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(
        name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user
    )
    c = Customer.objects.create(
        owner=user,
        name='Test Customer',
        email="customer@email.com",
        phone='02394943',
        address='Customer Address 25'
    )
    sale = Sale.objects.create(owner=user, product=p, customer=c, quantity=1, sale_date=date.today(), sale_price=1000.00)

    payload = {
        "product": p.name,
        "customer": c.name,
        "quantity": 3,
        "sale_date": date.today().isoformat(),
        "sale_price": "900.00"
    }

    url = reverse("sale-detail", args=[sale.id])
    response = api_client.put(url, data=payload, format="json")

    assert response.status_code == 200
    sale.refresh_from_db()
    assert sale.quantity == 3
    assert sale.total_price == 2700.00

@pytest.mark.django_db
def test_delete_own_sale(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user)
    c = Customer.objects.create(owner=user, name="Test Customer", email="t@t.bg", phone="1", address="X")
    sale = Sale.objects.create(owner=user, product=p, customer=c, quantity=1, sale_date=date.today(), sale_price=1000.00)

    url = reverse("sale-detail", args=[sale.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Sale.objects.filter(id=sale.id).exists()

@pytest.mark.django_db
def test_create_sale_invalid_data(api_client):
    user = User.objects.create_user(username="user1", password="pass")

    category = Category.objects.create(name='Electronics')
    product = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=10,
        category=category,
        owner=user)
    customer = Customer.objects.create(owner=user, name="Test Customer", email="a@a.bg", phone="123", address="test")
    api_client.force_authenticate(user=user)

    payload = {
        "product": "invalid_id", 
        "customer": customer.id,
        "quantity": "ten",
        "sale_date": "invalid-date",
        "sale_price": "abc" 
    }

    url = reverse("sale-list")
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 400