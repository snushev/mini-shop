import pytest
from MiniShopApp.models import Purchase, Product, Supplier, User, Category
from django.urls import reverse
from datetime import date

@pytest.mark.django_db
def test_create_purchase_success(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    category = Category.objects.create(name='Electronics')
    product = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user)
    supplier = Supplier.objects.create(
        owner=user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )
    api_client.force_authenticate(user=user)

    payload = {
        "product": product.name,
        "supplier": supplier.name,
        "quantity": 5,
        "purchase_date": date.today().isoformat(),
        "unit_cost_price": "3.50"
    }

    url = reverse("purchase-list")
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201
    assert Purchase.objects.filter(owner=user).count() == 1
    purchase = Purchase.objects.first()
    assert purchase.total_price == 17.50
    product.refresh_from_db()
    assert product.quantity_in_stock == 8

@pytest.mark.django_db
def test_purchase_list_only_user(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    other = User.objects.create_user(username="user2", password="pass2")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user)
    s = Supplier.objects.create(owner=user, name="Test", contact_email="t@t.bg", phone="1", address="X")
    Purchase.objects.create(owner=other, product=p, supplier=s, quantity=1, purchase_date=date.today(), unit_cost_price=1.0)

    response = api_client.get(reverse("purchase-list"))
    assert response.status_code == 200
    assert len(response.data["results"]) == 0

@pytest.mark.django_db
def test_get_single_purchase(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user)
    s = Supplier.objects.create(owner=user, name="Test", contact_email="t@t.bg", phone="1", address="X")

    purchase = Purchase.objects.create(owner=user, product=p, supplier=s, quantity=2, purchase_date=date.today(), unit_cost_price=2.0)

    url = reverse("purchase-detail", args=[purchase.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["total_price"] == "4.00"
    assert response.data["quantity"] == 2

@pytest.mark.django_db
def test_user_cannot_access_others_purchase(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    other = User.objects.create_user(username="user2", password="pass2")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user)
    s = Supplier.objects.create(owner=other, name="Test", contact_email="t@t.bg", phone="1", address="X")
    purchase = Purchase.objects.create(owner=other, product=p, supplier=s, quantity=2, purchase_date=date.today(), unit_cost_price=2.0)

    url = reverse("purchase-detail", args=[purchase.id])
    response = api_client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_update_own_purchase(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(
        name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user
    )
    s = Supplier.objects.create(
        owner=user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )
    purchase = Purchase.objects.create(owner=user, product=p, supplier=s, quantity=1, purchase_date=date.today(), unit_cost_price=1.0)

    payload = {
        "product": p.name,
        "supplier": s.name,
        "quantity": 10,
        "purchase_date": date.today().isoformat(),
        "unit_cost_price": "5.00"
    }

    url = reverse("purchase-detail", args=[purchase.id])
    response = api_client.put(url, data=payload, format="json")

    assert response.status_code == 200
    purchase.refresh_from_db()
    assert purchase.quantity == 10
    assert purchase.total_price == 50.0

@pytest.mark.django_db
def test_delete_own_purchase(api_client):
    user = User.objects.create_user(username="user1", password="pass")
    api_client.force_authenticate(user=user)

    category = Category.objects.create(name='Electronics')
    p = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user)
    s = Supplier.objects.create(owner=user, name="Test", contact_email="t@t.bg", phone="1", address="X")
    purchase = Purchase.objects.create(owner=user, product=p, supplier=s, quantity=1, purchase_date=date.today(), unit_cost_price=2.0)

    url = reverse("purchase-detail", args=[purchase.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Purchase.objects.filter(id=purchase.id).exists()

@pytest.mark.django_db
def test_create_purchase_invalid_data(api_client):
    user = User.objects.create_user(username="user1", password="pass")

    category = Category.objects.create(name='Electronics')
    product = Product.objects.create(name='Laptop',
        sku='ABC123',
        price=1200,
        quantity_in_stock=3,
        category=category,
        owner=user)
    supplier = Supplier.objects.create(owner=user, name="Test", contact_email="a@a.bg", phone="123", address="test")
    api_client.force_authenticate(user=user)

    payload = {
        "product": "invalid_id", 
        "supplier": supplier.id,
        "quantity": "ten",
        "purchase_date": "invalid-date",
        "unit_cost_price": "abc" 
    }

    url = reverse("purchase-list")
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 400
