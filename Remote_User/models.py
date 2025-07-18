from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)


class Cyber_model(models.Model):

    Name_of_Covered_Entity= models.CharField(max_length=30000)
    State= models.CharField(max_length=300)
    Individuals_Affected= models.CharField(max_length=300)
    Date_of_Breach= models.CharField(max_length=300)
    Location_of_Breached_Information= models.CharField(max_length=300)
    Date_Posted_or_Updated= models.CharField(max_length=300)
    breach_start= models.CharField(max_length=300)
    year= models.CharField(max_length=300)
    Source_Ip= models.CharField(max_length=300)
    Destination_Ip= models.CharField(max_length=300)
    Prediction= models.CharField(max_length=300)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



