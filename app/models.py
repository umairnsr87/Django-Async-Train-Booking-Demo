from django.db import models


# Create your models here.

class UserModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    userid = models.CharField(max_length=50, default="-----")

    def __str__(self):
        return str(self.name) + str(self.email) + str(self.password)


class LoginSession(models.Model):
    userid = models.IntegerField()
    email = models.EmailField(max_length=100)
    # token=models.CharField(max_length=100)
    lastlogin = models.DateTimeField()

    def __str__(self):
        return str(self.userid) + str(self.email) + str(self.lastlogin)


class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    availibility = models.BooleanField()
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.name) + "__" + str(self.source) + "__" + str(self.destination) + "__" + str(
            self.availibility) + "__" + str(self.capacity)


class Booking(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    train_name = models.CharField(max_length=100)
    train_id = models.EmailField(max_length=100)
    date = models.DateTimeField()
    status = models.BooleanField(default=False)
    source = models.CharField(max_length=100 )
    destination = models.CharField(max_length=100)
    passengers = models.IntegerField()

    def __str__(self):
        return str(self.username) + "__" + str(self.date) + "__" + str(self.status)
