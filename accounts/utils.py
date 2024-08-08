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

# for calender time zone

from datetime import datetime
import pytz

from datetime import datetime
import pytz

def convert_to_iso(datetime_input, timezone_str):
    # Check if datetime_input is a string or datetime object
    if isinstance(datetime_input, str):
        # Parse the input datetime string if it's a string
        dt = datetime.strptime(datetime_input, '%Y-%m-%d %H:%M:%S')
    elif isinstance(datetime_input, datetime):
        # Use the input datetime object directly if it's already a datetime object
        dt = datetime_input
    else:
        raise TypeError("datetime_input must be a str or datetime object")

    # Define the timezone
    timezone = pytz.timezone(timezone_str)

    # Localize the datetime (convert naive datetime to timezone-aware)
    if dt.tzinfo is None:
        localized_dt = timezone.localize(dt)
    else:
        # If the datetime is already timezone-aware, convert it to the desired timezone
        localized_dt = dt.astimezone(timezone)

    # Convert to ISO 8601 format with timezone
    iso_format_str = localized_dt.isoformat()
    
    return iso_format_str
