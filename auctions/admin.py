from django.contrib import admin
from .models import AuctionListings, Bids, Comments, User, ClosedListing

admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(ClosedListing)

# admin.site.register(Watchlist)
# Register your models here.
