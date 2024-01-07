from django.db import models

# Create your models here.
class Room(models.Model):
    id = models.UUIDField(verbose_name = "Oda Id")