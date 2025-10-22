from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from .models import OrderStatus
from django.http import Http404
from django.contrib import messages
from django.utils import timezone

def order_manager(request):
    orders = (Order.objects.filter(paid=True).
              exclude(order__status=OrderStatus.STATUS_DONE).
              select_related('order').order_by('-created'))
    return render(request,'warehouse/orders_pick.html',{'orders':orders})

def orders_done(request):
    orders = Order.objects.filter(order__status=OrderStatus.STATUS_DONE).select_related('order')
    return render(request,'warehouse/done_orders.html',{'orders': orders})

def order_detail(request, order_id):
    try:
        order = get_object_or_404(Order.objects.select_related('order'), id=order_id)
    except Http404:
        return redirect('warehouse:orders_manager')

    return render(request, 'warehouse/order_detail.html', {'order': order})


def assign_picker(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_status = OrderStatus.objects.get(order=order)

    # Проверяем, не назначен ли уже сборщик
    if order_status.picker:
        messages.warning(request, 'На этот заказ уже назначен сборщик')
    else:
        # Назначаем текущего пользователя сборщиком
        order_status.picker = request.user
        order_status.status = OrderStatus.STATUS_PROCESSING
        order_status.save()
        messages.success(request, 'Вы назначены сборщиком этого заказа')

    return redirect('warehouse:order_detail', order_id=order_id)


def update_order_items(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)

        # Получаем список собранных позиций
        collected_items = request.POST.getlist('collected_items')

        # Обновляем статус позиций заказа
        for item in order.items.all():
            if str(item.id) in collected_items:
                item.is_collected = True
            else:
                item.is_collected = False
            item.save()

        messages.success(request, 'Статус позиций обновлен')

    return redirect('warehouse:order_detail', order_id=order_id)


def complete_order(request, order_id):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=order_id)
            order_status = OrderStatus.objects.get(order=order)
        except Http404:
            return redirect('warehouse:orders_manager')

        # Проверяем, что все позиции собраны


        if order_status.picker == request.user:
            order_status.status = OrderStatus.STATUS_DONE
            order_status.picked = timezone.now()
            order_status.save()
            messages.success(request, 'Заказ успешно завершен!')
        else:
            messages.error(request, 'Не все позиции собраны или вы не являетесь сборщиком')

    return redirect('warehouse:order_detail', order_id=order_id)

def done_order_detail(request, order_id):
    try:
        order = get_object_or_404(Order.objects.select_related('order'), id=order_id)
    except Http404:
        return redirect('warehouse:orders_manager')

    return render(request, 'warehouse/done_order_detail.html', {'order': order})

def worker_stat(request):
    orders = Order.objects.filter(order__picker=request.user).order_by('order__picked')
    return render(request,'warehouse/worker_stat.html',{'orders': orders})