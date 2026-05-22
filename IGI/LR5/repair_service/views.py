import requests
import calendar
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserRegisterForm
from .models import Profile, Order, Device, Service


class ServiceListView(ListView):
    model = Service
    template_name = 'repair_service/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = Service.objects.select_related('category').all()
        search_query = self.request.GET.get('q', '')
        sort_by = self.request.GET.get('sort', '')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query) 
        
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('category', 'price')
            
        return queryset

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user, role='client',
                phone=form.cleaned_data['phone'], birth_date=form.cleaned_data['birth_date']
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    profile = request.user.profile
    context = {'profile': profile}

    try:
        nbrb_req = requests.get('https://api.nbrb.by/exrates/rates/431').json()
        context['usd_rate'] = nbrb_req.get('Cur_OfficialRate', 3.20)
    except:
        context['usd_rate'] = 3.20 

    try:
        time_req = requests.get('http://worldtimeapi.org/api/timezone/Europe/Minsk', timeout=3).json()
        context['current_time'] = time_req.get('datetime')[:10]
    except:
        context['current_time'] = timezone.now().date().isoformat()  

    now = datetime.now()
    cal = calendar.HTMLCalendar(calendar.MONDAY)
    context['html_calendar'] = cal.formatmonth(now.year, now.month)

    if profile.role == 'client':
        context['devices'] = Device.objects.filter(client=profile)
        context['orders'] = Order.objects.filter(client=profile).order_by('-created_at')
        
    elif profile.role == 'master':
        context['orders'] = Order.objects.filter(master=profile)
        
        all_orders = Order.objects.all()
        total_costs = [order.total_cost for order in all_orders if order.total_cost > 0]
        
        context['stats'] = {
            'total_orders': all_orders.count(),
            'avg_check': round(sum(total_costs)/len(total_costs), 2) if total_costs else 0,
        }

        status_counts = all_orders.values('status').annotate(count=Count('id'))
        context['chart_labels'] = [item['status'] for item in status_counts]
        context['chart_data'] = [item['count'] for item in status_counts]

    return render(request, 'repair_service/dashboard.html', context)

def create_superuser(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Ура! Суперпользователь 'admin' с паролем 'admin123' успешно создан! Можете заходить в /admin")
    return HttpResponse("Суперпользователь уже существует. Идите в /admin")

from .models import Article, CompanyInfo, FAQ, EmployeeContact, Vacancy, Review, PromoCode

def home(request):
    latest_article = Article.objects.order_by('-created_at').first()
    return render(request, 'repair_service/index.html', {'latest_article': latest_article})

def about(request):
    info = CompanyInfo.objects.first() 
    return render(request, 'repair_service/about.html', {'info': info})

def news_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'repair_service/news.html', {'articles': articles})

def news_detail(request, pk):
    article = Article.objects.get(id=pk)
    return render(request, 'repair_service/news_detail.html', {'article': article})

def faq_list(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'repair_service/faq.html', {'faqs': faqs})

def contacts(request):
    employees = EmployeeContact.objects.all()
    return render(request, 'repair_service/contacts.html', {'employees': employees})

def privacy(request):
    return render(request, 'repair_service/privacy.html') 

def vacancies(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'repair_service/vacancies.html', {'vacancies': vacancies})

def promo_codes(request):
    active_promos = PromoCode.objects.filter(is_active=True)
    archived_promos = PromoCode.objects.filter(is_active=False)
    return render(request, 'repair_service/promo.html', {
        'active_promos': active_promos, 'archived_promos': archived_promos
    })

def reviews(request):
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        if rating and text:
            Review.objects.create(author=request.user, rating=rating, text=text)
            return redirect('reviews')

    all_reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'repair_service/reviews.html', {'reviews': all_reviews})

# repair_service/views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ServiceForm, ServiceCategoryForm
from .models import Service, ServiceCategory
from .decorators import admin_required


@admin_required
def manage_services(request):
    """Панель управления услугами"""
    services = Service.objects.select_related('category').all()
    categories = ServiceCategory.objects.all()
    
    return render(request, 'repair_service/admin/manage_services.html', {
        'services': services,
        'categories': categories,
        'active_tab': 'services'
    })

@admin_required
def add_service(request):
    """Добавление новой услуги"""
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Услуга успешно добавлена!')
            return redirect('manage_services')
        else:
            messages.error(request, '⚠️ Пожалуйста, исправьте ошибки в форме')
    else:
        form = ServiceForm()
    
    return render(request, 'repair_service/admin/service_form.html', {
        'form': form,
        'title': 'Добавление услуги',
        'button_text': '➕ Добавить'
    })

@admin_required
def edit_service(request, pk):
    """Редактирование услуги"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Услуга "{service.name}" успешно обновлена!')
            return redirect('manage_services')
        else:
            messages.error(request, '⚠️ Пожалуйста, исправьте ошибки в форме')
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'repair_service/admin/service_form.html', {
        'form': form,
        'title': f'Редактирование услуги: {service.name}',
        'button_text': '💾 Сохранить',
        'service': service
    })

@admin_required
def delete_service(request, pk):
    """Удаление услуги"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(request, f'🗑️ Услуга "{service_name}" удалена!')
        return redirect('manage_services')
    
    return render(request, 'repair_service/admin/service_confirm_delete.html', {
        'service': service
    })


@admin_required
def manage_categories(request):
    """Панель управления категориями услуг"""
    categories = ServiceCategory.objects.all().order_by('name')
    
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Категория успешно добавлена!')
            return redirect('manage_categories')
    else:
        form = ServiceCategoryForm()
    
    return render(request, 'repair_service/admin/manage_categories.html', {
        'categories': categories,
        'form': form,
        'active_tab': 'categories'
    })

@admin_required
def delete_category(request, pk):
    """Удаление категории (только если нет связанных услуг)"""
    category = get_object_or_404(ServiceCategory, pk=pk)
    
    if request.method == 'POST':
        if category.service_set.exists():
            messages.error(
                request, 
                f'Нельзя удалить категорию "{category.name}", так как в ней есть услуги. '
                f'Сначала удалите или переместите услуги.'
            )
        else:
            category_name = category.name
            category.delete()
            messages.success(request, f'✅ Категория "{category_name}" удалена!')
        return redirect('manage_categories')
    
    return render(request, 'repair_service/admin/category_confirm_delete.html', {
        'category': category
    })