from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    item_price = models.DecimalField(max_digits=15,decimal_places=2)
    item_title = models.CharField(max_length=64)
    item_desc = models.CharField(max_length=1028)
    item_category = models.CharField(max_length=64)
    item_image = models.URLField(max_length=500)
    item_lister = models.ForeignKey(User, on_delete=models.CASCADE)
    item_status = models.CharField(max_length=6, choices = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED')
    ], default = "OPEN")

    def __str__(self):
        return f'{self.item_title}'

class Bid(models.Model):
    item_bid = models.DecimalField(max_digits=15,decimal_places=2)
    item_title = models.ForeignKey(Listing, related_name = 'Name', on_delete=models.CASCADE)
    price_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.item_title} : {self.item_bid} by {self.price_user}'

class Comment(models.Model):
    item_title = models.ForeignKey(Listing, on_delete=models.CASCADE)
    item_comment = models.CharField(max_length=500)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.comment_user} {self.item_title} : {self.item_comment}'

class Watchlist(models.Model):
    item_title = models.ForeignKey(Listing, on_delete=models.CASCADE)
    item_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_watching = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.item_title} : {self.item_user}'