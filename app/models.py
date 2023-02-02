from django.db import models

# Create your models here.

class Text(models.Model):
    file_name = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    