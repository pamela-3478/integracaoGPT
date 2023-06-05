from django.db import models

# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    email = models.TextField(max_length=255, unique=True, default=None)
    nome = models.TextField(max_length=255)
    senha = models.TextField(max_length=255)
