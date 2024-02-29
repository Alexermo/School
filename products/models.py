from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, related_name='products')
    start_datetime = models.DateTimeField()
    min_group_size = models.IntegerField()
    max_group_size = models.IntegerField()


    def __str__(self):
        return self.name

    def get_lessons(self):
        return self.lesson_set.all()

    @property
    def lessons(self):
        return self.get_lessons()


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    video_url = models.URLField()

    def __str__(self):
        return self.title



