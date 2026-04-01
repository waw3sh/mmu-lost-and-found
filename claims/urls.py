from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('', views.claims_list, name='claims_list'),
    path('create/<int:item_id>/', views.create_claim, name='create_claim'),
    path('<int:claim_id>/', views.claim_detail, name='claim_detail'),
]
