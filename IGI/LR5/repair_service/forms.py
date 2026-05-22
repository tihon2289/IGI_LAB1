from django import forms
from django.contrib.auth.models import User
from .models import Service, ServiceCategory
from .models import Profile
from datetime import date
import re

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    phone = forms.CharField(label='Телефон', help_text='Формат: +375 (29) XXX-XX-XX')
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError("Неверный формат телефона!")
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError("Регистрация доступна только с 18 лет!")
        return birth_date
    
class ServiceForm(forms.ModelForm):
    """Форма для добавления/редактирования услуги"""
    
    class Meta:
        model = Service
        fields = ['category', 'name', 'price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Замена экрана'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'category': 'Категория услуги',
            'name': 'Название услуги',
            'price': 'Стоимость (BYN)',
        }

class ServiceCategoryForm(forms.ModelForm):
    """Форма для добавления/редактирования категории услуг"""
    
    class Meta:
        model = ServiceCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Ремонт телефонов'}),
        }
        labels = {
            'name': 'Название категории',
        }
