import random
from django.core.mail import EmailMessage
from .models import User, UserCode
from django.conf import settings


def key_generate():
    code = ""
    for i in range(6):
        code += str(random.randint(1, 9))
    return code


def send_code(email):
    Subject = 'Код подтверждения'
    code = key_generate()
    print(code)
    user = User.objects.get(email=email)
    email_body = f"{user.username}, ваш код подтверждения {code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    UserCode.objects.create(user=user, code=code)
    message = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    message.send(fail_silently=True)
