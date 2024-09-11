import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from product.models import Product
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from user.models import User
from datetime import datetime


@receiver(post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    if kwargs['created']:
        subject = 'Product added'
        message = f'{instance.name} added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Product)
def pre_delete_customer(sender, instance, **kwargs):
    product_data = {
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'price': instance.price,
        'discount': instance.discount,
        'quantity': instance.quantity,
        'slug': instance.slug,
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'product/deleted_products', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(product_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
