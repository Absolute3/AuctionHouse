from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("item/<str:title>", views.page, name = "page"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("categories", views.categories, name = "category"),
    path("categories/<str:title>", views.category_list, name = "categorylist"),
    path("watchlist", views.user_watchlist, name = "watchlist"),
    path("bid/<str:title>", views.bid, name = "bid"),
    path("add_watchlist/<str:title>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<str:title>", views.remove_watchlist, name="remove_watchlist"),
    path("close_auction/<str:title>", views.close_auction, name="close_auction"),
    path("myauctions", views.myauctions, name="myauctions"),
]
