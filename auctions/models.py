from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"id:{self.id} | username:{self.username} | email:{self.email}" 

class Category(models.Model):
    name = models.TextField()
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.TextField()
    description = models.TextField()
    start_price = models.PositiveBigIntegerField()
    current_price = models.PositiveBigIntegerField(default=f"{int(0)}")
    picture_url = models.URLField()
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_DEFAULT, default = "", related_name='listing')
    activity = models.CharField(max_length=1, choices=[("A","Active"), ("C", "Closed")], default="A")
    date_time = models.DateTimeField(auto_now_add=True)

class ListingAdmin(admin.ModelAdmin):
    list_display= ('id', 'user_id', 'title', 'description', 'start_price', 'picture_url', 'activity', 'date_time')

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bid')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    price = models.PositiveBigIntegerField()
    def __str__(self):
        return f"listing:{self.listing_id} | user:{self.user_id} | price: {self.price}"

class Comments(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)



