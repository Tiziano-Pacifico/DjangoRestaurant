from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from foodOnline_main import settings

def detectUser(user):
    if user.role == 1:
        redicrectUrl = 'vendorDashboard'
        return redicrectUrl
    elif user.role == 2:
        redicrectUrl = 'custDashboard'
        return redicrectUrl
    elif user.role == None:
        redicrectUrl = '/admin'
        return redicrectUrl
    
def send_verification_email(request, user, mail_subject,email_template):

    print(mail_subject)
    from_email = settings.DEFAULT_FROM_EMAIL
    print(from_email)
    current_site = get_current_site(request)
    print(current_site)
    message = render_to_string(email_template, {
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    print(message)
    to_email = user.email
    print(to_email)
    mail = EmailMessage(mail_subject, message, from_email,to=[to_email])
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context['user'].email
    print(from_email)
    mail = EmailMessage(mail_subject, message, from_email,to=[to_email])
    mail.send()


