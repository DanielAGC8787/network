
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_post", views.create_post, name="create_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("test", views.test, name="test"),
    path("users/<str:username>", views.users, name="users"),
    path("following", views.following, name="following"),

    #API routes
    path("posts/<int:post_id>", views.post, name="post"),
    path("posts", views.all_posts, name="all_posts"), 
    path("get_current_user", views.get_current_user, name="get_current_user"),
    # the string you are sending here "followingUser" must be the same as the variable name in your views.py
    path("unfollow/<str:followingUser>", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("get_user/<str:user>", views.get_user, name="get_user"),
    path("get_user_posts/<str:username>", views.get_user_posts, name="get_user_posts"),
    path("following_list", views.following_list, name="following_list")

]
