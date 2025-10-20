from celery import shared_task


@shared_task
def get_confirm_code(user_id):
    from django.core.mail import send_mail
    from accounts.models import CustomUser, ActivationCode
    user = CustomUser.objects.get(id=user_id)
    activation = ActivationCode.objects.get(user=user)
    code = activation.code
    subject = f'Код активации для {user.username}'
    message = f'Код активации : {code}'
    mail_sent = send_mail(subject, message, 'admin@shop.ru', [user.email])
    return mail_sent