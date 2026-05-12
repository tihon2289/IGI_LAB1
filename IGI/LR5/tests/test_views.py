import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_page_status(client):
    # Проверяем, что главная страница открывается (код 200)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_services_page_status(client):
    # Проверяем страницу услуг
    url = reverse('services')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_redirects_anonymous_user(client):
    # Проверяем, что неавторизованного юзера кидает на страницу входа
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 302
    assert 'login' in response.url