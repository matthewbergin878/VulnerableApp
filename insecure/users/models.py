from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.username
