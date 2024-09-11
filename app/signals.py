import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from app.models import Author, Book
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from user.models import User
from datetime import datetime


@receiver(post_save, sender=Author)
def create_product(sender, instance, created, **kwargs):
    if kwargs['created']:
        subject = 'Author joined'
        message = f'{instance.name} joined.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Author)
def pre_delete_customer(sender, instance, **kwargs):
    author_data = {
        'id': instance.id,
        'name': instance.name,
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'app/deleted/author', f'{date}.json')

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(author_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Book)
def create_product(sender, instance, created, **kwargs):
    if kwargs['created']:
        subject = 'Book added'
        message = f'{instance.name} added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Book)
def pre_delete_customer(sender, instance, **kwargs):
    book_data = {
        'id': instance.id,
        'name': instance.name,
        'author': str(instance.author),
        'price': instance.price,
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'app/deleted/book', f'{date}.json')

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(book_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
