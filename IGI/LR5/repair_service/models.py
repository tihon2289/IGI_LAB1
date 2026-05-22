from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from .models import Service, ServiceCategory
from datetime import date


phone_validator = RegexValidator(
    regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
    message="Телефон должен быть в формате: +375 (29) XXX-XX-XX"
)

def validate_age_18_plus(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("Пользователю (клиенту или сотруднику) должно быть не менее 18 лет!")

class Profile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('master', 'Сотрудник (Мастер)'),
        ('admin', 'Администратор'), 
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

    @property
    def total_cost(self):
        services_cost = sum(service.price for service in self.services.all())
        parts_cost = sum(part.price for part in self.parts.all())
        return services_cost + parts_cost


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_desc = models.CharField(max_length=255, verbose_name="Краткое содержание (1 предложение)")
    content = models.TextField(verbose_name="Полный текст")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Картинка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новость/Статья"
        verbose_name_plural = "Новости"

class CompanyInfo(models.Model):
    text = models.TextField(verbose_name="Информация о компании")
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name="Логотип")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    history = models.TextField(blank=True, null=True, verbose_name="История по годам")
    requisites = models.TextField(blank=True, null=True, verbose_name="Реквизиты")

    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Вопрос-ответ (Термин)"
        verbose_name_plural = "Словарь терминов (FAQ)"

class EmployeeContact(models.Model):
    name = models.CharField(max_length=150, verbose_name="ФИО сотрудника")
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name="Фото")
    job_description = models.TextField(verbose_name="Описание работ")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Почта")

    class Meta:
        verbose_name = "Контакт сотрудника"
        verbose_name_plural = "Контакты сотрудников"

class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Актуальна?")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)] # Оценки от 1 до 5
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата отзыва")
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name="Фото к отзыву")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код купона")
    discount = models.CharField(max_length=100, verbose_name="Скидка/Описание")
    is_active = models.BooleanField(default=True, verbose_name="Действует (Не в архиве)")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды и купоны"


class ServiceForm(forms.ModelForm):
    """Форма для добавления/редактирования услуги"""
    
    class Meta:
        model = Service
        fields = ['category', 'name', 'price']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border-radius: 4px;'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border-radius: 4px;',
                'placeholder': 'Например: Замена экрана iPhone'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border-radius: 4px;',
                'placeholder': '0.00',
                'step': '0.01'
            }),
        }
        labels = {
            'category': 'Категория услуги',
            'name': 'Название услуги',
            'price': 'Стоимость (BYN)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not self.fields[field].widget.attrs.get('class'):
                self.fields[field].widget.attrs['class'] = 'form-control'


class ServiceCategoryForm(forms.ModelForm):
    """Форма для добавления/редактирования категории услуг"""
    
    class Meta:
        model = ServiceCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px; border-radius: 4px;',
                'placeholder': 'Например: Ремонт телефонов'
            }),
        }
        labels = {
            'name': 'Название категории',
        }