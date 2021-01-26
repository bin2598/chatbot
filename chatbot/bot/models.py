from django.db import models

class register(models.Model):
    name = models.CharField(max_length=10)
    phone = models.IntegerField()
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

class chat(models.Model):
    user = models.ForeignKey(register,on_delete=models.CASCADE)
    fat = models.IntegerField(default=0)
    stupid = models.IntegerField(default=0)
    dump = models.IntegerField(default=0)