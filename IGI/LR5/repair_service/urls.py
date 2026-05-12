from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    
    re_path(r'^services/$', views.ServiceListView.as_view(), name='services'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html', next_page='dashboard'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]