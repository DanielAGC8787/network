from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionListings(models.Model):
    class Category(models.TextChoices):
        shoes = "Shoes"
        hats = "Hats"
        jackets = "Jackets"
        toys = "Toys"
        shirts = "Shirts"
        pants = "Pants"
        accessories = "Accessories"
    name = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    description = models.TextField(max_length=1000)
    image_url = models.CharField(max_length=1000)
    category = models.CharField(choices=Category.choices, max_length=100)
    highest_bid = models.IntegerField(null=True)
    highest_bid_holder = models.CharField(max_length=64, null=True)
    creator = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Bids(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.amount}"

class User(AbstractUser):
    watchlist_listings = models.ManyToManyField(AuctionListings, blank=True, related_name="listings")

class Comments(models.Model):
    comment = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.comment}"

class ClosedListing(models.Model):
    class Category(models.TextChoices):
        shoes = "Shoes"
        hats = "Hats"
        jackets = "Jackets"
        toys = "Toys"
        shirts = "Shirts"
        pants = "Pants"
        accessories = "Accessories"
    name = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    description = models.TextField(max_length=1000)
    image_url = models.CharField(max_length=1000)
    category = models.CharField(choices=Category.choices, max_length=100)
    highest_bid = models.IntegerField(null=True)
    creator = models.CharField(max_length=64)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", null=True)
