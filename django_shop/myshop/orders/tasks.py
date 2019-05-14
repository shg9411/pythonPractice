from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'{order.first_name}씨, 주문이 완료되었습니다. 주문번호는 {order.id}입니다.'
    mail_sent = send_mail(subject, message, 'shg9411@naver.com', [order.email])
    return mail_sent
