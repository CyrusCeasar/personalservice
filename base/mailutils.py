from django.core.mail import send_mail
from django.conf import settings
import smtplib


def send_mail(to, subject, email_body):
    session = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    session.ehlo()
    session.starttls()
    session.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    recipient_list = [to, ]
    headers = "\r\n".join(["from: " + 'My Test Mail',
                           "subject: " + subject,
                           "mime-version: 1.0",
                           "content-type: text/html"])
    # body_of_email can be plaintext or html!
    content = headers + "\r\n\r\n" + email_body
    session.sendmail(settings.EMAIL_HOST_USER, recipient_list, content)

# def sendEmail(to,subject,message):
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [to,]
#     send_mail(subject, message, email_from, recipient_list )
