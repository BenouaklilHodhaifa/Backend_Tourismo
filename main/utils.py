from django.core.mail import send_mail

def send_newsletter_email(subject, message, recipient_list):
    send_mail(subject, message, 'john.doe.2023.example@gmail.com', recipient_list, fail_silently=False)