import time

from celery import shared_task
from django.core.mail import send_mail

from cinema.celery import app


@app.task
def send_confirmation_email(code,email):
    time.sleep(10)
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'

    send_mail(
        'привет',
        full_link,
        'bagdadzhunushov@gmail.com',
        [email],
    )