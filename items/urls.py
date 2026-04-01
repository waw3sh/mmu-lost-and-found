from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.items_list_view, name='items_list'),  # User's items with filtering
    path('register/', views.register_item_view, name='register'),
    path('my-items/', views.my_items, name='my_items'),
    path('create/', views.create_item, name='create_item'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
]
