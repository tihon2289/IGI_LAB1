import pytest
from repair_service.models import ServiceCategory, Service
from django.contrib.auth.models import User
from repair_service.models import Profile, Device, DeviceType, Order, PartCategory, SparePart
from datetime import date, timedelta

@pytest.mark.django_db
def test_service_creation():
    # Создаем тестовую категорию и услугу
    category = ServiceCategory.objects.create(name="Ремонт ПК")
    service = Service.objects.create(category=category, name="Чистка от пыли", price=50.00)
    
    # Проверяем, что данные сохранились корректно
    assert service.name == "Чистка от пыли"
    assert service.price == 50.00
    assert str(category) == "Ремонт ПК"

@pytest.mark.django_db
def test_order_total_cost():
    # 1. Создаем пользователя и профиль
    user = User.objects.create(username="client1")
    profile = Profile.objects.create(user=user, role='client', phone='+375 (29) 111-22-33', birth_date=date(1990, 1, 1))
    
    # 2. Создаем устройство
    dtype = DeviceType.objects.create(name="Ноутбук")
    device = Device.objects.create(client=profile, device_type=dtype, brand_model="Asus")
    
    # 3. Создаем Заказ
    order = Order.objects.create(
        contract_number="001", client=profile, device=device, 
        deadline=date.today() + timedelta(days=5)
    )
    
    # 4. Создаем 2 услуги (100 и 50 BYN) и 1 запчасть (200 BYN)
    scat = ServiceCategory.objects.create(name="Ремонт")
    service1 = Service.objects.create(category=scat, name="Замена экрана", price=100.00)
    service2 = Service.objects.create(category=scat, name="Чистка", price=50.00)
    
    pcat = PartCategory.objects.create(name="Матрицы")
    part1 = SparePart.objects.create(category=pcat, name="Экран IPS", price=200.00)
    
    # Добавляем их в заказ
    order.services.add(service1, service2)
    order.parts.add(part1)
    
    # 5. Итоговая сумма должна быть 350 BYN (100+50+200)
    assert order.total_cost == 350.00