# models.py
from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    father_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=10)
    class_field = models.CharField(max_length=20,default="")
    remarks = models.TextField()

    def __str__(self):
        return self.name
