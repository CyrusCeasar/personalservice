from datetime import  datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Vocabulary(models.Model):
    word = models.CharField(max_length=50, primary_key=True)
    display_content = models.TextField()
    src_content = models.TextField()

    def __str__(self):
        return self.words_text + "---" + self.display_content


class LookUpRecord(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    lookup_amount = models.IntegerField(default=0)
    last_lookup_time = models.DateTimeField(default=datetime.now)
    remembered = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    device_id = models.CharField(null=True, max_length=50)
    user_id = models.IntegerField(null=True)


class Device(models.Model):
    device_id = models.CharField(max_length=50, primary_key=True)
    device_type = models.CharField(max_length=50)
