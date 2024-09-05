from django.db import models
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    price = models.FloatField(null=True)
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_attributes(self):
        product_attributes = ProductAttribute.objects.filter(product=self)
        attributes = []
        for product_attribute in product_attributes:
            attributes.append({
                'attribute_key': product_attribute.attribute.key_name,
                'attribute_value': product_attribute.attribute_value.value_name
            })
        return attributes

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name


class Image(BaseModel):
    image = models.ImageField(upload_to='images/products', null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, related_name='images', null=True)


class Attribute(BaseModel):
    key_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.key_name


class AttributeValue(BaseModel):
    value_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.value_name


class ProductAttribute(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('AttributeValue', on_delete=models.CASCADE)


class Commit(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    user_name = models.CharField(max_length=125)
    user_email = models.CharField(max_length=125)
    body = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.user_name} for {self.product.name}"