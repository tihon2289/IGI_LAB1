from django.contrib import admin
from .models import (
    Profile, ServiceCategory, Service, PartCategory, 
    SparePart, DeviceType, Device, Order
)

# --- 1. Встроенное редактирование (Inlines) ---
# Позволяет добавлять услуги прямо на странице создания категории
class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

class SparePartInline(admin.TabularInline):
    model = SparePart
    extra = 1

# --- 2. Регистрация справочников ---
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ServiceInline] # Подключаем встроенное редактирование

@admin.register(PartCategory)
class PartCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [SparePartInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# --- 3. Регистрация основных сущностей ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'birth_date')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'phone')

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('brand_model', 'client', 'device_type', 'serial_number')
    list_filter = ('device_type',)
    search_fields = ('brand_model', 'serial_number', 'client__user__username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'client', 'master', 'status', 'deadline', 'get_total_cost')
    list_filter = ('status', 'created_at')
    search_fields = ('contract_number', 'client__user__username')
    
    # Делаем удобный интерфейс выбора для полей Многие-ко-многим
    filter_horizontal = ('services', 'parts') 
    
    # Поле итоговой стоимости доступно только для чтения
    readonly_fields = ('get_total_cost',)

    # Вывод свойства total_cost в админке
    def get_total_cost(self, obj):
        return f"{obj.total_cost} BYN"
    get_total_cost.short_description = "Итоговая сумма"