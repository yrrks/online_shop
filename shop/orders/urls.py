from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('payment/<int:order_id>/', views.imitation_payment, name='imitation_payment'),
]