from django.db import models

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class User(models.Model):
    name=models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Complaints(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.CharField(max_length=50)
    complaints = models.CharField(max_length=700)
    reply = models.CharField(max_length=700)
    status = models.CharField(max_length=30)
