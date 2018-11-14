from django.db import models

# Create your models here.


class BlogsPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()


class JsonPost(models.Model):
    classid = models.CharField(max_length=150)
    jsonfile = models.FileField(upload_to='json/')


