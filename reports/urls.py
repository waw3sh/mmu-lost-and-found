from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('found/<uuid:item_uuid>/', views.finder_page, name='finder_page'),
    path('reports/', views.reports_list_view, name='list'),
]
