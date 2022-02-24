from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, User, Bid, Comment, Watchlist
from django import forms 
from django.contrib.auth.decorators import login_required

class bidplace(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['item_bid']
        
class commentplace(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['item_comment']
        labels = {
            'item_comment' : ('Add your comment'),
        }
        attrs = {
            'size': '1000',
        }
        
class listingplace(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_title','item_price', 'item_desc', 'item_category', 'item_image']

def index(request):
    mess = Listing.objects.filter(item_status = "OPEN")
    return render(request, "auctions/index.html",{
        "message": mess
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


def page(request, title):
    try:
        mess =  Listing.objects.get(item_title = title) 
        listings = Watchlist.objects.filter(item_user = request.user, is_watching=True).values('item_title')
        list = Listing.objects.filter(id__in = listings)
        watch = Watchlist.objects.filter(item_user = request.user, item_title = mess).values('is_watching')
        topbid = Bid.objects.filter(item_title = mess).first()
        if request.method == "POST":
            if commentplace(request.POST).is_valid():
                comment = request.POST.get("item_comment")
                if comment != "":
                    Comment.objects.create(comment_user = request.user, item_comment = comment, item_title = mess)
                    return HttpResponseRedirect(reverse("page", args = (title,)))
        if(request.user == mess.item_lister and mess.item_status == "OPEN"):
            return render(request, "auctions/page.html", {
                "message": mess,
                "list" : list,
                "watch" : watch,
                "commentform" : commentplace(),
                "comments": Comment.objects.filter(item_title = mess.id),
                "owner" : True,
                "topbid" : topbid
             })
        elif mess.item_status == "OPEN":
            return render(request, "auctions/page.html", {
                "bidform" : bidplace(),
                "message": mess,
                "list" : list,
                "watch" : watch,
                "commentform" : commentplace(),
                "comments": Comment.objects.filter(item_title = mess.id),
                "owner" : False,
                "topbid" : topbid
             })
        else:
            test = Bid.objects.filter(item_title = mess).first()
            if(test.price_user == request.user):
                return render(request, "auctions/page.html", {
                "message": mess,
                "list" : list,
                "watch" : watch,
                "comments": Comment.objects.filter(item_title = mess.id),
                "owner" : False,
                "topbid" : topbid,
                "closed" : True,
                "topbidholder" : True
                })
            return render(request, "auctions/page.html", {
                "message": mess,
                "list" : list,
                "watch" : watch,
                "comments": Comment.objects.filter(item_title = mess.id),
                "owner" : False,
                "topbid" : topbid,
                "closed" : True,
                "topbidholder" : False
             })
    except:
        return render(request, "auctions/page.html", {
            "message": mess,
            "comments": Comment.objects.filter(item_title = mess.id),
            "bids" :Bid.objects.filter(item_title = mess.id)})


@login_required(login_url='/login')
def bid(request,title):
    if request.method == "POST":
        form = request.POST["item_bid"]
        form = float(form)
        mess = Listing.objects.get(item_title = title).item_price
        item = Listing.objects.get(item_title = title)
        price = Bid.objects.filter(item_title = item)
        if price:
            check = Bid.objects.get(item_title = item).item_bid
            if form > float(check):
                Bid.objects.filter(item_title = item).update(item_bid = form, price_user = request.user)
                return HttpResponseRedirect(reverse("page", args = (title,)))
            else:
                return HttpResponse("Bid is too low")
        else:
            if form > float(mess):
                Bid.objects.create(item_title = item, item_bid = form, price_user = request.user)
                return HttpResponseRedirect(reverse("page", args = (title,)))
            else:
                return HttpResponse("Bid is too low")
                
                
@login_required(login_url='/login')
def createlisting(request):
    if request.method == "POST":
        form = listingplace(request.POST, request.FILES)
        if form.is_valid():
            item = form.cleaned_data['item_title']
            price = form.cleaned_data['item_price']
            desc = form.cleaned_data['item_desc']
            category = form.cleaned_data['item_category']
            image = form.cleaned_data['item_image']
            instances = form.save(commit=False)
            instances.item_user = request.user
            category = category.title()
            Listing.objects.create(item_title = item, item_price = price, item_desc = desc, item_category = category, item_image = image, item_lister = request.user, item_status = "OPEN")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createlisting.html",{"form": form})
    return render(request, "auctions/createlisting.html", {"form": listingplace()})


def categories(request):
    check = Listing.objects.values('item_category').distinct().filter(item_status = "OPEN")
    return render(request, "auctions/category.html",{
        "message": check
    })


def category_list(request,title):
    check = Listing.objects.filter(item_category = title, item_status = "OPEN")
    return render(request,"auctions/category.html",{
        "content": check,
        "mm" : title
    })


@login_required(login_url='/login')
def add_watchlist(request,title):
    mess = Listing.objects.filter(item_title = title)
    if mess:
        x = Watchlist(item_title=mess.first(),is_watching=True,item_user=request.user)
        x.save()
    else:
        Watchlist.objects.create(item_user = request.user, item_title = title, is_watching = True)
    return HttpResponseRedirect(reverse("page", args = (title,)))


@login_required(login_url='/login')
def remove_watchlist(request,title):
    mess = Listing.objects.filter(item_title = title)
    if mess:
        Watchlist.objects.filter(item_title=mess.first(),is_watching=True,item_user=request.user).delete()
    return HttpResponseRedirect(reverse("page", args = (title,)))


@login_required(login_url='/login')
def user_watchlist(request):
    listings = Watchlist.objects.filter(item_user = request.user, is_watching=True).values('item_title')
    list = Listing.objects.filter(id__in = listings)
    return render(request, "auctions/watchlist.html",{
        "message": list
        })


@login_required(login_url='/login')
def close_auction(request,title):
    mess = Listing.objects.filter(item_title = title)
    if mess:
        Listing.objects.filter(item_title = mess.first()).update(item_status = "CLOSED")
    return HttpResponseRedirect(reverse("page", args = (title,)))


@login_required(login_url='/login')
def myauctions(request):
    listings = Listing.objects.filter(item_lister = request.user)
    if listings:
        open = Listing.objects.filter(item_lister = request.user, item_status = "OPEN")
        close = Listing.objects.filter(item_lister = request.user, item_status = "CLOSED")
        return render(request, "auctions/myauctions.html",{
        "open": open,
        "closed": close
        })
    else:
        return render(request, "auctions/myauctions.html",{
        "message": "No listings"
        })