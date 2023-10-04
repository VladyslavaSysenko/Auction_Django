# **Commerce**

This is e-commerce auction site based on Django that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist”.

---

## **Detailed description**

You can either read or watch a video https://youtu.be/BZY0Q-iYa58

>***Active Listings Page***: The default route let users view all of the currently active auction listings. If the user is signed in, they can be added to watchlist.
>
>***Create Listing***: Users can visit a page to create a new listing. They must specify a title for the listing, a text-based description and the starting bid. Users can optionally provide a URL for an image for the listing and/or a category (can be chosed from existing or created a new one).
>
>***Listing Page***: Clicking on a listing takes users to a page specific to that listing. On that page, users can view all details about the listing.
If the user is signed in, the user can add comments, add or remove the item to their “Watchlist” as well as bid on the item. 
Creator of the listing can close the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
>
>***Watchlist***: Users who are signed in can visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes user to that listing’s page.
>
>***Categories***: Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.
>
>***Django Admin Interface***: Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.
---
## **To start the app**

- Cd into the commerce directory. 
- Run ***pip install -r requirements.txt*** to install all requirements.
- Run ***python manage.py runserver*** to start up the Django web server, and visit the website in your browser.

You can register as usual user or log into superuser via  
username - *superuser*  
password - *superuser*  
and go to http://127.0.0.1:8000/admin/ to see django admin interface.

---
## **To change database**

- In your terminal, cd into the commerce directory. 
- Run ***python manage.py makemigrations auctions*** to make migrations for the auctions app.
- Run ***python manage.py migrate*** to apply migrations to your database.