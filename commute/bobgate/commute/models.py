from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Department(models.Model):
    department = models.CharField(null = False, max_length = 30)
    def __str__(self):
        return self.department


class Employee(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, default = 1, on_delete = models.CASCADE)


class Work(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()