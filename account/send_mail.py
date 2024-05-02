from django.core.mail import send_mail
from django.utils.html import format_html


def send_confirmation_email(email, code):
    message = format_html(
        'Здравствуйте, активируйте ваш аккаунт! Ваш код активации: <strong>{}</strong>.<br>Не передавайте этот код '
        'никому.',
        code)
    send_mail(
        "Здравствуйте, активируйте ваш аккаунт!",
        message,
        'shopapiviewadmin@gmail.com',
        [email],
        fail_silently=False,
    )
