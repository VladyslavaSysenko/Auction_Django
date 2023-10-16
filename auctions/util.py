from .models import Listing


def escape(s):
    """
    Escape special characters.

    https://github.com/jacebrowning/memegen#special-characters
    """
    for old, new in [
        ("-", "--"),
        (" ", "-"),
        ("_", "__"),
        ("?", "~q"),
        ("%", "~p"),
        ("#", "~h"),
        ("/", "~s"),
        ('"', "''"),
    ]:
        s = s.replace(old, new)
    return s


def current_bid(listing_id):
    try:
        bid = max(
            list(Listing.objects.get(id=listing_id).bid.all().values_list("price", flat=True))
        )
    except ValueError:
        bid = 0
    return bid
