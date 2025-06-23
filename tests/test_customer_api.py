import pytest
from MiniShopApp.models import Customer
from django.urls import reverse

@pytest.mark.django_db
def test_list_customers(api_client, create_user):
    user = create_user(username='user1', password='password2')
    api_client.force_authenticate(user=user)

    Customer.objects.create(
        owner=user,
        name='Test',
        email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    response = api_client.get(reverse('customer-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Test'
    assert response.data['results'][0]['email'] == 'test@email.com'

    
@pytest.mark.django_db
def test_user_cannot_retrieve_other_clients_list(api_client, create_user):
    user = create_user(username='user1', password='password2')
    other_user = create_user(username='user2', password='password3')
    api_client.force_authenticate(user=user)

    customer = Customer.objects.create(
        owner=other_user,
        name='Test',
        email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    response = api_client.get(reverse('customer-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_create_customer_success(api_client, create_user):
    user = create_user(username="test", password='password1')
    api_client.force_authenticate(user=user)

    payload = {
        'name':'Test',
        'email':'test@test.ts',
        'phone':'123',
        'address':'TestTest'
    }

    url = reverse('customer-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201
    assert Customer.objects.filter(name='Test', owner=user, phone='123').exists()

@pytest.mark.django_db
def test_create_customer_wrong_data_type_fails(api_client, create_user):
    user = create_user(username="test", password='password1')
    api_client.force_authenticate(user=user)

    payload = {
        'name':123,
        'email':123,
        'phone':'123',
        'address':'TestTest'
    }

    url = reverse('customer-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_retrieve_customer(api_client, create_user):
    user = create_user(username='test', password='password')
    api_client.force_authenticate(user=user)

    customer = Customer.objects.create(
        owner=user,
        name='Test',
        email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    url = reverse('customer-detail', args=[customer.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == 'Test'
    assert response.data['email'] == 'test@email.com'

@pytest.mark.django_db
def test_user_cannot_access_other_users_customers(api_client, create_user):
    user = create_user(username='test', password='password')
    other_user = create_user(username='test1', password='password1')
    api_client.force_authenticate(user=user)

    customer = Customer.objects.create(
        owner=other_user,
        name='Test',
        email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    url = reverse('customer-detail', args=[customer.id])
    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_own_customer(api_client, create_user):
    user = create_user(username='user1', password='pass')
    api_client.force_authenticate(user=user)

    customer = Customer.objects.create(
        owner=user,
        name='Test',
        email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    new_data = {
        'name':'New Name',
        'email':'test1@test.ts',
        'phone':'1234',
        'address':'TestTest'
    }
    url = reverse('customer-detail', args=[customer.id])
    response = api_client.put(url, new_data , format='json')

    assert response.status_code == 200

    customer.refresh_from_db()
    assert customer.name == 'New Name'
    assert customer.phone == '1234'

@pytest.mark.django_db
def test_delete_own_customer(api_client, create_user):
    user = create_user(username='user1', password='pass')
    api_client.force_authenticate(user=user)

    customer = Customer.objects.create(
        owner=user,
        name='Test',
        email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    url = reverse('customer-detail', args=[customer.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Customer.objects.filter(id=customer.id).exists()