import requests
import calendar
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Count, Avg
from .forms import UserRegisterForm
from .models import Profile, Order, Device, Service

def home(request):
    return render(request, 'repair_service/index.html')

# 1. ПОИСК И СОРТИРОВКА (Обновляем ServiceListView)
class ServiceListView(ListView):
    model = Service
    template_name = 'repair_service/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = Service.objects.select_related('category').all()
        # Получаем параметры из URL (?q=...&sort=...)
        search_query = self.request.GET.get('q', '')
        sort_by = self.request.GET.get('sort', '')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query) # Поиск по имени
        
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('category', 'price')
            
        return queryset

def register(request):
    # ... твой текущий код регистрации остается без изменений ...
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

# 2. API, СТАТИСТИКА И ВИЗУАЛИЗАЦИЯ (Обновляем dashboard)
@login_required
def dashboard(request):
    profile = request.user.profile
    context = {'profile': profile}

    # --- API 1: Курс Доллара (Нацбанк РБ) ---
    try:
        nbrb_req = requests.get('https://api.nbrb.by/exrates/rates/431').json()
        context['usd_rate'] = nbrb_req.get('Cur_OfficialRate', 3.20)
    except:
        context['usd_rate'] = 3.20 # Резервное значение, если нет интернета

    # --- API 2: Точное время (WorldTimeAPI) ---
    try:
        time_req = requests.get('http://worldtimeapi.org/api/timezone/Europe/Minsk').json()
        context['current_time'] = time_req.get('datetime')[:10] # Берем только дату
    except:
        context['current_time'] = datetime.now().strftime('%Y-%m-%d')

    # Текстовый календарь (требование методички)
    now = datetime.now()
    cal = calendar.HTMLCalendar(calendar.MONDAY)
    context['html_calendar'] = cal.formatmonth(now.year, now.month)

    # --- Разграничение прав и Статистика ---
    if profile.role == 'client':
        context['devices'] = Device.objects.filter(client=profile)
        context['orders'] = Order.objects.filter(client=profile).order_by('-created_at')
        
    elif profile.role == 'master':
        context['orders'] = Order.objects.filter(master=profile)
        
        # СТАТИСТИКА
        all_orders = Order.objects.all()
        # Для расчета средних значений используем генератор списков (list comprehension)
        total_costs = [order.total_cost for order in all_orders if order.total_cost > 0]
        
        context['stats'] = {
            'total_orders': all_orders.count(),
            'avg_check': round(sum(total_costs)/len(total_costs), 2) if total_costs else 0,
        }

        # Данные для диаграммы Chart.js (группировка по статусам)
        status_counts = all_orders.values('status').annotate(count=Count('id'))
        context['chart_labels'] = [item['status'] for item in status_counts]
        context['chart_data'] = [item['count'] for item in status_counts]

    return render(request, 'repair_service/dashboard.html', context)