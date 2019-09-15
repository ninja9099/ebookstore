import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.exceptions import APIException
from apps.users.models import EmailVerificationTokens

logger = logging.getLogger('api')

def get_verification_email_context(user, req_email):

    template_str = 'emails/verification_email.html'
    username = user.username
    host = settings.EMAIL_VERIFY_HOST
    from_email =  settings.EMAIL_HOST_USER
    html_path = template_str
    token, created = EmailVerificationTokens.objects.get_or_create(user=user, is_active=True)
    active_link = 'http://%s/verify_email/?token=%s&user=%s' % (
        host, token.key, token.user.username)

    context = {
        'username': username,
        'host': host,
        'from_email': from_email,
        'html_path': html_path,
        'subject': "E-bookstore - Verify Account",
        'active_link': active_link,
        'reply_to': "noreply@ebook.com",
        'send_to': [req_email],
    }
    return context

def send_verification_email(context=None):

    subject = context['subject']
    from_email = context['from_email']
    message = render_to_string(context['html_path'], context)

    try:
        logger.info('Sending mail to user email {}'.format(context['send_to']))
        res =  send_mail(subject, message, from_email, context['send_to'])
        logger.info('Response from mail client:\n {}'.format(res))
        return res
    except Exception as e:
        print(str(e))
        logger.critical('Exception occurred in file {}'.format(__file__), exc_info=True)
        raise APIException('Unable to send email please try again later')