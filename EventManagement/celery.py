import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

# set the default Django settings module for the 'celery' program.
from django.conf import settings
from django.template.loader import render_to_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RituEventManagement.settings')
from django.core.mail import send_mail

app = Celery('RituEventManagement', broker='pyamqp://guest@localhost//')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def send_email(to, subject, image_url, context):
    image_data = open(image_url, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_USER
    msg['To'] = to

    string = render_to_string('EventManagement/registration_email.html', context)
    text = MIMEText(string, 'html')
    msg.attach(text)
    image = MIMEImage(image_data, name="QR-Code")
    msg.attach(image)

    server = smtplib.SMTP(settings.EMAIL_HOST+":"+settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)

    server.sendmail(settings.EMAIL_USER, to, msg.as_string())
    server.quit()
    return

