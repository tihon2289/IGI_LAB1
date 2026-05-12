import pytest
from datetime import date, timedelta
from repair_service.forms import UserRegisterForm

@pytest.mark.django_db
def test_valid_registration_form():
    past_date = date.today() - timedelta(days=20*365)
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
        'phone': '+375 (29) 111-22-33',
        'birth_date': past_date.strftime('%Y-%m-%d')
    }
    form = UserRegisterForm(data=data)
    assert form.is_valid() == True

@pytest.mark.django_db
def test_invalid_phone_registration_form():
    past_date = date.today() - timedelta(days=20*365)
    data = {
        'username': 'testuser2',
        'password': 'testpassword123',
        'phone': '80291112233', 
        'birth_date': past_date.strftime('%Y-%m-%d')
    }
    form = UserRegisterForm(data=data)
    assert form.is_valid() == False
    assert 'phone' in form.errors

@pytest.mark.django_db
def test_underage_registration_form():
    past_date = date.today() - timedelta(days=10*365)
    data = {
        'username': 'testuser3',
        'password': 'testpassword123',
        'phone': '+375 (29) 111-22-33',
        'birth_date': past_date.strftime('%Y-%m-%d')
    }
    form = UserRegisterForm(data=data)
    assert form.is_valid() == False
    assert 'birth_date' in form.errors