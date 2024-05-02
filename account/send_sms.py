from twilio.rest import Client
from django.conf import settings
import random


# password = U5yb4v'KpeX!_gYgeq1 twilio
def generate_sms_code():
    return ''.join(str(random.randint(0, 9)) for _ in range(4))


def sending_sms(phone_number, activate_code):

    text = f'Ваш код активации {activate_code}'
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
            body=text,
            from_=settings.TWILIO_SENDER_PHONE,
            to=phone_number
        )
    print(message.status)
    return 'The message was successfully sent!'
