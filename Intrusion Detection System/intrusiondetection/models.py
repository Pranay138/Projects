from django.db import models
from django.db.models import Model

class UserModel(Model):

    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)

    class Meta:
        db_table = "registration model"