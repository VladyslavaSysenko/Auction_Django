from django.contrib import admin

from .models import Bid, Comments, User, Listing, ListingAdmin, Category, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comments)