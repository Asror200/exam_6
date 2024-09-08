from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.author}'