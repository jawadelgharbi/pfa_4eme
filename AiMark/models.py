from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User

# Create your models here.


fs = FileSystemStorage(location='/marks')


class MyMark(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marks")
    nom = models.CharField(max_length=100, null=False)
    image = models.ImageField(max_length=100, null=False, upload_to='marks/')
    desctiption = models.CharField(max_length=500, null=False)
    gravit = models.IntegerField(null=False)
    date = models.DateField(default=datetime.now, null=False)

    def __str__(self):
        return self.nom


class MyPoint(models.Model):
    mymark = models.ForeignKey(MyMark, related_name='points', on_delete=models.CASCADE)
    numero = models.IntegerField(null=False, default=1)
    x = models.FloatField(null=False)
    y = models.FloatField(null=False)
