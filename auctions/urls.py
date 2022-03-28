from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("unauthorized_page", views.unauthorized_page, name="unauthorized_page"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("listing/<int:listing_id>/watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/<int:listing_id>/remove_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listing/<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("won_listings/<str:username>", views.won_listings, name="won_listings"),
    path("won_listing/<int:listing_id>", views.won_listing, name="won_listing")

]
