from celery import shared_task


@shared_task
def order_created(order_id):
    from django.core.mail import send_mail
    from orders.models import Order
    order = Order.objects.get(id=order_id)
    items_text = "Состав заказа:\n"
    for item in order.items.all():
        items_text += f"- {item.product.name}: {item.quantity} × {item.price} руб. = {item.get_cost()} руб.\n"
    subject = f'Заказ № {order.id}'
    message = f'''
Заказ № {order.id} успешно зарегистрирован на сумму {float(order.get_global_cost())} рублей

{items_text}

Данные для доставки:
Имя: {order.first_name} {order.last_name}
Адрес: {order.city}, {order.address}, индекс: {order.postal_code}



'''
    if order.paid:
        message += """
Благодарим за заказ!
Ожидайте доставку в ближайшее время!
"""
    else:
        message += '''
Не забудьте оплатить заказ!
Заказ будет передан для доставки сразу после оплаты!
        '''

    mail_sent = send_mail(subject, message, 'admin@myshop.ru', [order.email])
    return mail_sent