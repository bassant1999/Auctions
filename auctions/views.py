
from asyncio.windows_events import NULL
from importlib.metadata import EntryPoint
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *


def index(request):
    listings = Listing.objects.filter(active=1)
    return render(request, "auctions/index.html", {"listings":listings})


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

# categories 
def categories(request):
    listings = Listing.objects.filter(active=1)
    Categories = Listing.objects.values_list('category').distinct()
    categories = []
    for i in range(len(Categories)):
        categories.append(Categories[i][0])
    return render(request, "auctions/categories.html", {"listings":listings, "categories":categories})

def category(request, name):
    Categories = Listing.objects.values_list('category').distinct()
    categories = []
    for i in range(len(Categories)):
        categories.append(Categories[i][0])
    listings = Listing.objects.filter(active=1,category=name)
    return render(request, "auctions/category.html", {"listings":listings, "categories":categories, "name":name})

#listing
def listing(request, id):
    listing = Listing.objects.get(id= id)
    owner = listing.owner
    comments = Comment.objects.filter(listing=listing)
    bids = Bid.objects.filter(listing=listing)
    bidsnum = len(bids)
    max = 0
    buser = 0
    if len(bids) > 0:
        buser = bids[0].cuser
        for b in bids:
            if b.price > max:
                max = b.price
                buser = b.cuser
    return render(request, "auctions/listing.html", {"listing":listing, "owner":owner, "comments":comments, "noOfBids":bidsnum, "cuser":buser})

def comment(request, lid, uid):
    l = Listing.objects.get(id= lid)
    cu = User.objects.get(id= uid)
    c = request.POST["comment"]
    comm =  Comment(cuser=cu, listing=l, Comment=c)
    comm.save()
    messages.success(request, 'your comment has been added succesfully.')
    return redirect("../"+str(lid))

def bid(request, lid, uid):
    l = Listing.objects.get(id= lid)
    cu = User.objects.get(id= uid)
    price = request.POST["price"]
    #get maximum bid
    bids = Bid.objects.filter(listing=l)
    max = 0
    buser = uid
    if len(bids) > 0:
        buser = bids[0].cuser
        for b in bids:
            if b.price > max:
                max = b.price
                buser = b.cuser
    if (float(price) >= l.price) and (float(price) > max):
        nbid = Bid(cuser=cu, listing=l, price=price)
        nbid.save()
        l.price = price
        l.save()
        messages.success(request, 'your bid has been added succesfully.')
        return redirect("../../"+str(lid))
    else:
        messages.add_message(request, messages.WARNING, 'the bid must be higher the current price.')
        return redirect("../../"+str(lid))
    nbid = Bid(cuser=cu, listing=l, price=price)
    print(nbid.cuser)
    # comm =  Comment(cuser=cu, listing=l, Comment=c)
    # comm.save()
    return redirect("../../"+str(lid))

def viewProfile(request, uid):
    user = User.objects.get(id=uid)
    clisting = Listing.objects.order_by('active').filter(owner=user)
    nbids = len(Bid.objects.filter(cuser=user))
    return render(request, "auctions/profile.html", {"clistings":clisting, "nlistings":len(clisting), "username":user.username, "nbids":nbids, "uid":uid})

### create listing
def create_listing(request, uid):
    if request.method == 'POST':
        user = User.objects.get(id=uid)
        l = 0
        if 'img' in request.FILES:
            image = request.FILES['img']
            next_id = 1
            if len(Listing.objects.all()):
                next_id = Listing.objects.order_by('-id').first().id + 1
            image.name = "img"+str(next_id)+"."+(image.name).split(".")[1]
            l = Listing(title=request.POST["title"], description=request.POST["desc"], price=float(request.POST["price"]),category=request.POST["category"], owner=user, img_url=image, active=1)
            l.save()
        else:
            l = Listing(title=request.POST["title"], description=request.POST["desc"], price=float(request.POST["price"]),category=request.POST["category"], owner=user, img_url=NULL, active=1)
            l.save()
        return redirect("../../listing/"+str(l.id))
    return render(request, 'auctions/add.html', {})

# watchlist
def addToWatchlist(request,uid,lid):
    user = User.objects.get(id=uid)
    list = Listing.objects.get(id=lid)
    wlists = Watchlist.objects.filter(cuser=user, listing=list)
    if(len(wlists) != 0 ):
        messages.add_message(request, messages.WARNING, 'you have added this item to the watchlist previously')
        return redirect("../../listing/"+str(lid))
    watchlist = Watchlist(cuser=user,listing=list)
    watchlist.save()
    messages.success(request, 'added succesfully.')
    return redirect("../../listing/"+str(lid))

def watchlist(request,uid):
    user = User.objects.get(id=uid)
    watchlists = Watchlist.objects.filter(cuser=user)
    return render(request, 'auctions/watchlist.html', {"watchlists":watchlists})

def remove(request,lid,uid):
    user = User.objects.get(id=uid)
    list = Listing.objects.get(id=lid)
    wl = Watchlist.objects.filter(cuser=user, listing=list)
    wl.delete()
    messages.success(request, 'Removed succesfully.')
    return redirect("../../watchlist/"+str(uid))

# inactivate
def inactivate(request,uid,lid):
    list = Listing.objects.get(id=lid)
    list.active = 0
    list.save()
    #get user of maximum bid
    bids = Bid.objects.filter(listing = list)
    max = 0
    user = User.objects.get(id=uid)
    for b in bids:
        if b.price > max:
            max = b.price
            user = b.cuser
    notify = Notifications(cuser=user, notification = "you have won "+str(list.title), list=list)
    notify.save()
    messages.success(request, 'inactivated succesfully.')
    return redirect("../../listing/"+str(lid))

# notifications
def notify(request,uid):
    user = User.objects.get(id=uid)
    notifications = Notifications.objects.filter(cuser=user)
    return render(request, 'auctions/notifications.html', {"notifications":notifications})