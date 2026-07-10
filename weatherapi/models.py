from django.db import models

# Create your models here.
class Weather(models.Model):
    city=models.CharField(max_length=150)
    country=models.CharField(max_length=100)
    temperature=models.FloatField()
    humidity=models.IntegerField()
    wind_speed=models.FloatField()
    weather_condition=models.CharField(max_length=150)
    search_date=models.DateField(auto_now_add=True)
    search_time=models.TimeField(auto_now_add=True)



class Signup(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=150,unique=True)
    password=models.CharField(max_length=10)
    cpassword=models.CharField(max_length=10)