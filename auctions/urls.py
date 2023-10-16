from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing_<str:listing_id>", views.listing_page, name="listing_page"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.category_page, name="category_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create_listing, name="create_listing"),
    path("comment", views.comment, name="comment"),
    path("close", views.close, name="close"),
    path("delete", views.delete, name="delete"),
]
