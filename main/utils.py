from django.core.mail import send_mail
from .models import SubscriberRegion, SubscriberVille

def send_newsletter_email(subject, message, recipient_list):
    send_mail(subject, message, 'john.doe.2023.example@gmail.com', recipient_list, fail_silently=False)


def send_newsletter_region(region, event_name, date, description):
    subject = f' Exciting New Event in {region}'

    message = 'Hello! This is a notification from our newsletter.'

    recipient_list = []
    subscribers = SubscriberRegion.objects.filter(region=region)
    for subscriber in subscribers:
        recipient_list.append(subscriber.email) 
    send_newsletter_email(subject, message, recipient_list)

def send_newsletter_ville(ville, event_name, date, description):
    subject = f'Newsletter Notification about the city: {ville}'
    message = 'Hello! This is a notification from our newsletter.'
    recipient_list = []
    subscribers = SubscriberVille.objects.filter(ville=ville)
    for subscriber in subscribers:
        recipient_list.append(subscriber.email)
    send_newsletter_email(subject, message, recipient_list)
    