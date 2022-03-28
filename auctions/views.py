from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings, Bids, Comments, ClosedListing

class NewTaskForm(forms.ModelForm): #create  new form
    class Meta:
        model = AuctionListings
        fields = ['name', 'starting_bid', 'description', 'image_url', 'category'] #this is what determine the order of the fields in the web app

class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

class WatchlistForm(forms.Form):
    #Booleanfield works as checkmark CheckboxInput Specifies what will be sent and onchange submits form
    is_watchlist = forms.BooleanField(label="Watchlist", widget=forms.CheckboxInput(attrs={'onchange': 'submit();'}))

# this is_valid method will work as validation for the amount submission
def is_valid(amount, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if listing.highest_bid is None:
        if amount<=listing.starting_bid:
            return False
        return True
    if amount <= listing.highest_bid or amount<=listing.starting_bid:
        return False
    return True

def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": AuctionListings.objects.all(),

    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def unauthorized_page(request):
    return render(request, "auctions/unauthorized_page.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": AuctionListings.Category
    })

# the argument 'category' must be 'category'. The code will not work if you use another name. This
# is bc the link sends 'category' as its argument and the view expects that exact same argument back
def category(request, category):
    return render(request, "auctions/category_listing.html", {
        "category": category,
        "listings": AuctionListings.objects.all()
    })

def watchlist(request, username):
    user = User.objects.get_by_natural_key(username)
    return render(request, "auctions/watchlist.html", {
        "watchlist" : user.watchlist_listings.all()
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        name = request.POST["name"]
        starting_bid = request.POST["starting_bid"]
        starting_bid = int(starting_bid)
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        creator = request.user.username
        if form.is_valid():
            AuctionListings.objects.create(name=name, starting_bid=starting_bid, description=description, image_url=image_url, category=category, creator=creator)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    return render(request, "auctions/create_listing.html", {
        "form": NewTaskForm()
    })

@login_required
def listing(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    user = request.user
    watchlist =user.watchlist_listings.all()
    in_watchlist = False
    if listing in watchlist:
        in_watchlist = True
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "num_bids": len(listing.bids.all()),
        "highest_bid": listing.highest_bid,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "comments": listing.comments.all(),
        "watchlist_form": WatchlistForm(),
        "in_watchlist": in_watchlist
        # "is_watchlist": listing.
    })

def bid(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if request.method == "POST":
        #make the amount returned from the form equal to amount
        amount = request.POST["amount"]
        amount = int(amount)
        #created my own validation for the amount
        if is_valid(amount, listing_id):
            # create a new bids record with the amount as amount and listing as listing
            Bids.objects.create(amount=amount, listing=listing)
            # make highest bid equal to amount
            listing.highest_bid = amount
            listing.highest_bid_holder = request.user.username
            # save this updated version of the listing
            listing.save()
            return HttpResponseRedirect(reverse("listing", args={listing_id}))
            # args must always be in brackets
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids": listing.bids.all(),
                "highest_bid": listing.highest_bid,
                "bid_form": BidForm(),
                "comment_form": CommentForm(),
                "comments": listing.comments.all(),
                "message": "The bid must be greater than the current bid"
            })

def comment(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if request.method == "POST":
        # make the comment returned from the form equal to comment
        comment = request.POST["comment"]
        # create a new bids record with the amount as amount and listing as listing
        Comments.objects.create(comment=comment, listing=listing, user = request.user)
        # save this updated version of the listing
        return HttpResponseRedirect(reverse("listing", args={listing_id}))
        # args must always be in brackets

def add_to_watchlist(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if request.method == "POST":
        user = request.user
        user.watchlist_listings.add(listing)
        return HttpResponseRedirect(reverse("listing", args={listing_id}))

def remove_from_watchlist(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    user = request.user
    user.watchlist_listings.remove(listing)
    return HttpResponseRedirect(reverse("listing", args={listing_id}))

def close_listing(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if request.method == "POST":
        name = listing.name
        starting_bid = listing.starting_bid
        description = listing.description
        image_url = listing.image_url
        category = listing.category
        highest_bid = listing.highest_bid
        winner = User.objects.get_by_natural_key(listing.highest_bid_holder)
        creator = listing.creator
        ClosedListing.objects.create(name=name, starting_bid=starting_bid, description=description, image_url=image_url,
                                     category=category, highest_bid=highest_bid, creator=creator, winner=winner)
        AuctionListings.delete(listing)
        return render(request, "auctions/close_listing_message.html")

def won_listings(request, username):
    user = User.objects.get_by_natural_key(username)
    return render(request, "auctions/won_listings.html", {
        "won_listings" : user.won_listings.all()
    })

def won_listing(request, listing_id):
    listing = ClosedListing.objects.get(id=listing_id)
    return render(request, "auctions/closed_listing.html", {
        "listing": listing
    })