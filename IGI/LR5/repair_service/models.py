from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date

# 1. КАСТОМНЫЕ ВАЛИДАТОРЫ (Из задания: Телефон и Возраст 18+)

# Регулярное выражение для телефона
phone_validator = RegexValidator(
    regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
    message="Телефон должен быть в формате: +375 (29) XXX-XX-XX"
)

# Функция для проверки возраста (18+)
def validate_age_18_plus(birth_date):
    today = date.today()
    # Считаем возраст с учетом високосных годов
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("Пользователю (клиенту или сотруднику) должно быть не менее 18 лет!")

# 2. ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (Связь 1:1 с базовым User)
class Profile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('master', 'Сотрудник (Мастер)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client', verbose_name="Роль")
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Номер телефона")
    birth_date = models.DateField(validators=[validate_age_18_plus], verbose_name="Дата рождения")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес проживания")
    passport_data = models.CharField(max_length=100, blank=True, null=True, verbose_name="Паспортные данные")
    specialization = models.CharField(max_length=100, blank=True, null=True, verbose_name="Специализация (только для мастеров)")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


# 3. СПРАВОЧНИКИ: УСЛУГИ И ЗАПЧАСТИ (Связи 1:M)

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип услуги")

    class Meta:
        verbose_name = "Тип услуги"
        verbose_name_plural = "Типы услуг"

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Наименование услуги")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Стоимость (BYN)")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} - {self.price} BYN"

class PartCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Вид запчасти")

    class Meta:
        verbose_name = "Вид запчасти"
        verbose_name_plural = "Виды запчастей"

    def __str__(self):
        return self.name

class SparePart(models.Model):
    category = models.ForeignKey(PartCategory, on_delete=models.CASCADE, verbose_name="Категория запчасти")
    name = models.CharField(max_length=200, verbose_name="Наименование запчасти")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена (BYN)")

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"

    def __str__(self):
        return f"{self.name} ({self.price} BYN)"


# 4. УСТРОЙСТВА И ЗАКАЗЫ (Договоры)

class DeviceType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Вид устройства (ноутбук, принтер и т.д.)")

    class Meta:
        verbose_name = "Вид устройства"
        verbose_name_plural = "Виды устройств"

    def __str__(self):
        return self.name

class Device(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'client'}, verbose_name="Владелец (Клиент)")
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, verbose_name="Тип")
    brand_model = models.CharField(max_length=150, verbose_name="Марка и модель")
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Серийный номер")

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    def __str__(self):
        return f"{self.brand_model} (Владелец: {self.client.user.username})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает мастера'),
        ('in_progress', 'В ремонте'),
        ('completed', 'Готов'),
        ('cancelled', 'Отменен'),
    ]

    contract_number = models.CharField(max_length=20, unique=True, verbose_name="Номер договора")
    client = models.ForeignKey(Profile, related_name='client_orders', on_delete=models.CASCADE, limit_choices_to={'role': 'client'}, verbose_name="Клиент")
    master = models.ForeignKey(Profile, related_name='master_orders', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'master'}, verbose_name="Назначенный мастер")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="Устройство")
    
    # Связи Многие-ко-многим (ManyToManyField)
    services = models.ManyToManyField(Service, blank=True, verbose_name="Оказанные услуги")
    parts = models.ManyToManyField(SparePart, blank=True, verbose_name="Использованные запчасти")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата заключения")
    deadline = models.DateField(verbose_name="Срок выполнения")

    class Meta:
        verbose_name = "Договор/Заказ"
        verbose_name_plural = "Договоры и Заказы"

    def __str__(self):
        return f"Договор №{self.contract_number} от {self.created_at}"

    # Функция автоматического подсчета итоговой суммы (Требование из методички)
    @property
    def total_cost(self):
        services_cost = sum(service.price for service in self.services.all())
        parts_cost = sum(part.price for part in self.parts.all())
        return services_cost + parts_cost