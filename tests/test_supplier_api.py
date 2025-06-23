
import pytest
from MiniShopApp.models import Supplier
from django.urls import reverse

@pytest.mark.django_db
def test_list_supplier(api_client, create_user):
    user = create_user(username='user1', password='password2')
    api_client.force_authenticate(user=user)

    Supplier.objects.create(
        owner=user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    response = api_client.get(reverse('supplier-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Test'

    
@pytest.mark.django_db
def test_user_cannot_retrieve_other_suppliers_list(api_client, create_user):
    user = create_user(username='user1', password='password2')
    other_user = create_user(username='user2', password='password3')
    api_client.force_authenticate(user=user)

    Supplier.objects.create(
        owner=other_user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    response = api_client.get(reverse('supplier-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_create_supplier_success(api_client, create_user):
    user = create_user(username="test", password='password1')
    api_client.force_authenticate(user=user)

    payload = {
        'name':'Test',
        'contact_email':'test@test.ts',
        'phone':'123',
        'address':'TestTest'
    }

    url = reverse('supplier-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201
    assert Supplier.objects.filter(name='Test', owner=user, phone='123').exists()

@pytest.mark.django_db
def test_create_supplier_wrong_data_type_fails(api_client, create_user):
    user = create_user(username="test", password='password1')
    api_client.force_authenticate(user=user)

    payload = {
        'name':[123],
        'contact_email':'test@test.ts',
        'phone':123,
        'address':'TestTest'
    }

    url = reverse('supplier-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_retrieve_supplier(api_client, create_user):
    user = create_user(username='test', password='password')
    api_client.force_authenticate(user=user)

    supplier = Supplier.objects.create(
        owner=user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == 'Test'
    assert response.data['contact_email'] == 'test@email.com'

@pytest.mark.django_db
def test_user_cannot_access_other_users_supplier(api_client, create_user):
    user = create_user(username='test', password='password')
    other_user = create_user(username='test1', password='password1')
    api_client.force_authenticate(user=user)

    supplier = Supplier.objects.create(
        owner=other_user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_own_supplier(api_client, create_user):
    user = create_user(username='user1', password='pass')
    api_client.force_authenticate(user=user)

    supplier = Supplier.objects.create(
        owner=user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    new_data = {
        'name':'New Name',
        'contact_email':'test1@test.ts',
        'phone':'1234',
        'address':'TestTest'
    }
    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.put(url, new_data , format='json')

    assert response.status_code == 200

    supplier.refresh_from_db()
    assert supplier.name == 'New Name'
    assert supplier.phone == '1234'

@pytest.mark.django_db
def test_delete_own_supplier(api_client, create_user):
    user = create_user(username='user1', password='pass')
    api_client.force_authenticate(user=user)

    supplier = Supplier.objects.create(
        owner=user,
        name='Test',
        contact_email="test@email.com",
        phone='02394943',
        address='Testovo, Testova str. 25'
    )

    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Supplier.objects.filter(id=supplier.id).exists()