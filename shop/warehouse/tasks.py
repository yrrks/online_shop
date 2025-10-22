from celery import shared_task


@shared_task
def picked_done(order_id):
    from django.core.mail import send_mail
    from accounts.models import CustomUser
    from orders.models import Order

    order = Order.objects.get(id=order_id)
    user = order.user


    subject = f'заказ №{order_id} собран'
    message = f'''заказ №{order_id} для аккаунта {user.username} собран,
               в скором времени будет отправлен, спасибо за покупку!'''
    mail_sent = send_mail(subject, message, 'admin@shop.ru', [user.email])
    return mail_sent