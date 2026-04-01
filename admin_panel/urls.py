from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('admin-panel/', views.admin_overview, name='overview'),
    path('admin-panel/users/', views.admin_users, name='users'),
    path('admin-panel/items/', views.admin_items, name='items'),
    path('admin-panel/disputes/', views.admin_disputes, name='disputes'),
]
