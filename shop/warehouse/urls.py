from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [

    path('done/', views.orders_done, name='orders_done'),
    path('for_picking/', views.order_manager, name='orders_manager'),
    path('order_detail/<int:order_id>/',views.order_detail, name='order_detail'),
    path('order/<int:order_id>/assign/', views.assign_picker, name='assign_picker'),
    path('order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    path('done_order_detail/<int:order_id>/',views.done_order_detail, name='done_order_detail'),
    path('worker_stat/',views.worker_stat, name='worker_stat'),

]