from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_admin_notification(subject, message):
    admin_emails = [admin[1] for admin in settings.ADMINS]
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        admin_emails,
        fail_silently=False,
    )

def send_registration_confirmation_email(user_email, user_name):
    subject = 'Confirmation de votre demande d\'inscription - MedLink'
    html_message = render_to_string('emails/registration_confirmation.html', {
        'user_name': user_name,
        'support_email': settings.SUPPORT_EMAIL
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
        fail_silently=False,
    )

def send_registration_approved_email(user_email, user_name, temporary_password):
    subject = 'Votre compte MedLink a été approuvé'
    html_message = render_to_string('emails/registration_approved.html', {
        'user_name': user_name,
        'temporary_password': temporary_password,
        'login_url': settings.FRONTEND_URL + '/login'
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
        fail_silently=False,
    )
