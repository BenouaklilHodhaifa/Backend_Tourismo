from django.core.mail import send_mail
from .models import SubscriberRegion, SubscriberVille

def send_newsletter_email(subject, message, recipient_list):
    send_mail(subject, message,
            #    'john.doe.2023.example@gmail.com', 
            'tourismoapp@gmail.com',
               recipient_list, fail_silently=False)


def send_newsletter_region(region, event_name, date, description):
    subject = f'Exciting New Event in {region}'

    message = f"""Exciting news! We\'ve got an incredible event coming up in your area that we don\'t want you to miss. Check out the details below:\n
Event: {event_name}
Date: {date}
Time: event time

Description:{description}
Join us for this awesome event and have a blast! Get more info on our website.
Don't miss out on this amazing opportunity! See you at the event.

Cheers,

Tourismo team
    """

    recipient_list = []
    subscribers = SubscriberRegion.objects.filter(region=region)
    for subscriber in subscribers:
        recipient_list.append(subscriber.email) 
    send_newsletter_email(subject, message, recipient_list)

def send_newsletter_ville(ville, event_name, date, description):
    subject = f'Exciting New Event in {ville}'
    message = f"""Exciting news! We\'ve got an incredible event coming up in your area that we don\'t want you to miss. Check out the details below:\n
Event: {event_name}
Date: {date}
Time: event time

Description:{description}
Join us for this awesome event and have a blast! Get more info on our website.
Don't miss out on this amazing opportunity! See you at the event.

Cheers,

Tourismo team
    """
    recipient_list = []
    subscribers = SubscriberVille.objects.filter(ville=ville)
    for subscriber in subscribers:
        recipient_list.append(subscriber.email)
    send_newsletter_email(subject, message, recipient_list)
    