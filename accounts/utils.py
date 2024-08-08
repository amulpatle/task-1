from django.contrib.sites.shortcuts import get_current_site


# email sending 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


from django.conf import settings

def detectUser(user):
    if  user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
# def send_notification(mail_subject, mail_template, context):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     message = render_to_string(mail_template, context)
    
#     # Ensure to_email is a string
#     if isinstance(context['to_email'], str):
#         to_email = [context['to_email']]  # Create a list with the email string
#     else:
#         to_email = context['to_email']  # If it's already a list, use it as is

#     mail = EmailMessage(mail_subject, message, from_email, to=to_email)
#     mail.content_subtype = "html"
#     mail.send()

def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    
    
    to_email = [context['to_email']] if isinstance(context['to_email'], str) else context['to_email']

    # Create and send the email
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"  
    mail.send()

