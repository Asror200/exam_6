from django.db import models
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Customers(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/customer/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.email)
        super(Customers, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def joined(self):
        return f'{self.created_at.day} {self.created_at.month} {self.created_at.year}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Customers"

