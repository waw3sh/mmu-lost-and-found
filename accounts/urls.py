from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('test-sms/', views.test_sms_view, name='test_sms'),
    path('create-admin/', views.create_admin_view, name='create_admin'),
    path('public-users/', views.public_users_view, name='public_users'),
    path('make-admin/', views.create_production_admin, name='create_production_admin'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]
