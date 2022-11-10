from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Bid, Comments, User, Listing, Category, Watchlist
from . import util


# active listing page (page with all active listings)
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(activity="A"),
        "title": "Active listings"
    })

# show listing page
def listing_page(request, listing_id, winner=None, error_text=None):
        # check if page was not deleted
        try:
            # process bids
            if request.method == "POST":
                error_text = bid(request)
            else:
                # show winner if closed
                if Listing.objects.get(id=listing_id).activity == "C":
                    try:
                        winner = Bid.objects.filter(listing_id=Listing.objects.get(id=listing_id)).order_by('-price').first().user_id.username
                    except AttributeError:
                        winner = "No one"
            # show listing
            return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(id=listing_id),
                    "winner": winner,
                    "error_text": error_text
                })
        except Listing.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

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

# show list of categories or add if new
def list_categories(add=None):
    categories = Category.objects.values_list("name", flat=True)
    lower_categories = [c.casefold() for c in categories]
    if add:
        if add.casefold() not in lower_categories:
            categ = Category(name=add.capitalize())
            categ.save()
    active_categories_id = list(Listing.objects.filter(activity="A").values_list('category', flat=True))
    active_categories = Category.objects.filter(id__in = active_categories_id).values_list("name", flat=True)
    print(f"active {active_categories}")
    return (sorted(active_categories))

# create listing
@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        # if category is empty - No category
        catg = request.POST['category']
        if catg == "":
            catg = "No category"
        # add category to list of categories if new
        list_categories(catg)
        # add empty photo if not provided
        picture = request.POST['picture_url']
        if picture == "":
            picture = "https://www.vill.ogasawara.tokyo.jp/wp-content/themes/ogasawara/img/access/no_image.png"
        # submit creation of listing
        new = Listing(
            user_id=User.objects.get(id=request.user.id),
            title = request.POST['title'].capitalize(),
            description = request.POST['description'].capitalize(),
            start_price = request.POST['start_price'],
            picture_url = picture, 
            category = Category.objects.get(name=catg.capitalize())
            )
        new.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        # show page where to create the listing
        return render(request, "auctions/create.html", {
            "categories": list_categories()
        })

# show page with all categories
def categories(request):
    return render(request, "auctions/categories.html", {
            "categories": list_categories()
        })

# show all listings from category
def category_page(request, category_name):
    return render(request, "auctions/index.html", {
        "listings": Category.objects.get(name=category_name).listing.all().filter(activity="A"),
        "title": f'Category "{category_name}"'
    })


# watchlist
@login_required(login_url="login")
def watchlist(request):
    user_id = request.user.id
    # add to watchlist
    if request.method == "POST":
        listing = request.POST['listing']
        user_watchlist = Watchlist.objects.filter(user_id=user_id)
        user_listings = [str(x.listing.id) for x in user_watchlist]
        # add to watchlist
        if listing not in user_listings:
            new = Watchlist(
            user_id=User.objects.get(id=user_id),
            listing = Listing.objects.get(id=listing)
            )
            new.save()
            return JsonResponse({"done":"done"})
        # delete from watchlist
        else:
            delete = Watchlist.objects.get(user_id=user_id, listing=Listing.objects.get(id=listing))
            delete.delete()
            return JsonResponse({"done":"done"})
    # show watchlist
    else:
        try:
            return render(request, "auctions/index.html", {
                "listings": [x.listing for x in Watchlist.objects.filter(user_id=user_id)],
                "title": "Watchlist"
            })
        except Watchlist.DoesNotExist:
            #show empty watchlist
            return render(request, "auctions/index.html", {"title": "Watchlist"})

# my listings
@login_required(login_url="login")
def my_listings(request):
    return render(request, "auctions/index.html", {
                "listings": Listing.objects.filter(user_id=User.objects.get(id=request.user.id)),
                "title": "My listings"
            })
        
# add a bid
@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        user_id = User.objects.get(id=request.user.id)
        listing_id = request.POST['listing']

        # if bid not a number
        try:
            bid = int(request.POST['bid'])
        except:
            return util.escape("It's not an integer!")

        # if bid less than starting price
        if bid < int(Listing.objects.get(id=listing_id).start_price):
            return util.escape('Bid is less than starting price')

        print(f"bid{bid}")
        print(f"price{Bid.objects.filter(listing_id=listing_id).order_by('-price').all().values}")

        # if bid less than another bid
        try:
            if bid <= Bid.objects.filter(listing_id=listing_id).order_by('-price').first().price:
                return util.escape('Bid is not bigger than existing bid')
                

        except (Bid.DoesNotExist, AttributeError) as error:
            pass

        # add a bid
        new = Bid(
            user_id = user_id,
            listing_id = Listing.objects.get(id=listing_id),
            price = bid
        )
        new.save()

        # add current price to the listing
        listing = Listing.objects.get(id=listing_id)
        listing.current_price = bid
        listing.save() 

# make a comment
@login_required(login_url="login")
def comment(request):
    if request.method == "POST":
        new = Comments(
            user_id = User.objects.get(id=request.user.id),
            listing_id = Listing.objects.get(id=request.POST['listing_id']),
            comment = request.POST['comment']
        )
        new.save()

        # return to the listing page
        return HttpResponseRedirect(reverse("listing_page", args=(request.POST['listing_id'],)))

# close the auction
@login_required(login_url="login")
def close(request):
    if request.method == "POST":
        user = request.user.id
        listing_id = request.POST["listing_id"]
        creator = Listing.objects.get(id=listing_id).user_id.id
        # change activity to "closed"
        if user == creator:
            listing = Listing.objects.get(id=listing_id)
            listing.activity = "C"
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(request.POST['listing_id'],)))

# delete the listing
@login_required(login_url="login")
def delete(request):
    listing = Listing.objects.get(id=request.POST["listing_id"])
    category = Category.objects.get(name=listing.category).listing.filter(activity="A")
    listing.delete()
    # check if the last listing in the category
    if len(category) == 0:
        Category.objects.get(name=listing.category).delete()
    return HttpResponseRedirect(reverse("index"))
