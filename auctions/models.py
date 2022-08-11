from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    category = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
    ## New
    img_url = models.ImageField(upload_to='images/', null=True)
    active = models.IntegerField(null=True)
    ##End
    def __str__(self):
        return f"{self.title} ({self.description}) ({self.date})"

class Comment(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cowner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    Comment = models.CharField(max_length=400)

class Bid(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bowner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="blisting")
    price = models.FloatField()

class Watchlist(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wowner")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="wlisting")

class Notifications(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nowner")
    notification = models.CharField(max_length=400)
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="nlisting")

