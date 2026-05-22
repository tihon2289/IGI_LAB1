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
    path('make-admin/', views.create_superuser),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('faq/', views.faq_list, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('promo/', views.promo_codes, name='promo'),
    path('admin-panel/services/', views.manage_services, name='manage_services'),
    path('admin-panel/services/add/', views.add_service, name='add_service'),
    path('admin-panel/services/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('admin-panel/services/<int:pk>/delete/', views.delete_service, name='delete_service'),
    
    path('admin-panel/categories/', views.manage_categories, name='manage_categories'),
    path('admin-panel/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]