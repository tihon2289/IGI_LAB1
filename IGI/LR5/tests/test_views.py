import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_page_status(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_services_page_status(client):
    url = reverse('services')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_redirects_anonymous_user(client):
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 302
    assert 'login' in response.url