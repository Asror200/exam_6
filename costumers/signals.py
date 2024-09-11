import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from costumers.models import Customers
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from user.models import User
from datetime import datetime


@receiver(post_save, sender=Customers)
def post_save_customers(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'Customer joined'
        message = f'{instance.full_name} joined.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Customers)
def pre_delete_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
        'image': str(instance.image),
        'slug': instance.slug,
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'costumers/deleted_customers', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(customer_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
