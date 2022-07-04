from email.message import EmailMessage
from json import JSONDecodeError
from multiprocessing.sharedctypes import Value
import time, json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Post, User, Follower, Following
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from django.core.paginator import Paginator

class PostForm(forms.ModelForm): #create  new form
    class Meta:
        model = Post
        fields = ['body'] #this is what determine the order of the fields in the web app

def index(request):
    all_posts = Post.objects.all().order_by('-timeStamp')   
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/index.html", {
        "form": PostForm(),
        'page_obj': page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def create_post(request):
    if request.method == "POST":
        body = request.POST["body"]
        timeStamp = "" + date.today().strftime("%B %d, %Y") + ", " + datetime.today().strftime("%I:%M %p")
        Post.objects.create(body=body, creator=request.user, timeStamp=timeStamp, likes=0)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html", {
        "form": PostForm()
    })

def all_posts(request):
    currentUser = request.user.username
    posts = Post.objects.all()
    allPosts = []
    for post in posts:
        augmented_post = post.serialize()
        augmented_post['currentUser'] = currentUser
        allPosts.append(augmented_post)

    allPosts.reverse()
    return JsonResponse([post for post in allPosts], safe=False)

def following_list(request):
    followedPosts = []
    following = request.user.followings.all()
    allPosts = Post.objects.all()
    for post in allPosts:
        for user in following:
            user1 = User.objects.get_by_natural_key(user)
            if post.creator == user1 :
                followedPosts.append(post)
    followedPosts.reverse()
    return JsonResponse([post.serialize() for post in followedPosts], safe=False)

def get_user_posts(request, username):
    currentUser = request.user.username
    desiredUser = User.objects.get_by_natural_key(username)
    usersPosts = desiredUser.posts.all()
    usersPosts2 = []
    for post in usersPosts:
        augmented_post = post.serialize()
        augmented_post['currentUser'] = currentUser
        usersPosts2.append(augmented_post)
    usersPosts2.reverse()
    return JsonResponse([post for post in usersPosts2], safe=False)

@csrf_exempt
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") is not None:
            post.liked = data["liked"]
        if data.get("likes") is not None:
            post.likes = data["likes"]
        if data.get("body") is not None:
            post.body = data["body"]
        post.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def get_current_user(request):
    try:
        currentUser = User.objects.get_by_natural_key(request.user.username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Users not found."}, status=404)
    if request.method == "GET":
        serializer = UserSerialzer(currentUser)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

@csrf_exempt
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        followingUser = data.get("following", "")
        try:
            followedUser = User.objects.get_by_natural_key(followingUser)
        except User.DoesNotExist:
            return JsonResponse({"error": "Users not found."}, status=404)
        
        follower = Following(
            owner = request.user,
            following = followingUser
        )
        follower.save()

        following = Follower(
            owner = followedUser,
            follower = request.user.username
        )
        following.save()

        return JsonResponse({"message": "Followed successfully."}, status=201)

@csrf_exempt            
def unfollow(request, followingUser):
    try:
        following = Following.objects.get(owner = request.user, following = followingUser)
    except Following.DoesNotExist:
        return JsonResponse({"error": "Follow relationship not found."}, status=404)

    try:
        unfollowedUser = User.objects.get_by_natural_key(followingUser)
    except User.DoesNotExist:
        return JsonResponse({"error": "User to unfollow not found"})

    try:
        followed = Follower.objects.get(owner = unfollowedUser, follower = request.user.username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Followed relationship not found"})

    if request.method == "GET":
        return JsonResponse(following.serialize())

    elif request.method == "DELETE":
        following.delete()
        followed.delete()
        return JsonResponse({"message": "Deleted Following relationship successfully"})

def get_user(request, user):
    try: 
        theUser = User.objects.get_by_natural_key(user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"})

    if request.method == "GET":
        serializer = UserSerialzer(theUser)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def test(request):
    return render(request, "network/test.html")

def users(request, username):
    hasFollowed = False
    desiredUser = User.objects.get_by_natural_key(username)
    if request.user.is_authenticated:
        userFollowings = request.user.followings.all()
        for user in userFollowings:
            try:
                person = User.objects.get_by_natural_key(user)
            except User.DoesNotExist:
                hasFollowed = False
            if desiredUser == person:
                hasFollowed = True
    usersPosts = desiredUser.posts.all().order_by('-timeStamp')
    paginator = Paginator(usersPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/user.html", {
        "page_obj": page_obj,
        "desiredUser": desiredUser, 
        "following": len(desiredUser.followings.all()),
        "followers": len(desiredUser.followers.all()),
        "hasFollowed": hasFollowed
    })

def following(request):
    followedPosts = []
    following = request.user.followings.all()
    allPosts = Post.objects.all()
    for post in allPosts:
        for user in following:
            user1 = User.objects.get_by_natural_key(user)
            if post.creator == user1 :
                followedPosts.append(post)
    followedPosts.reverse()
    paginator = Paginator(followedPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": followedPosts,
        'page_obj': page_obj
    })

def edit_post(request, post_id):
    post = Post.objects.get(pk = post_id)
    body = post.body
    return render("network/index.html", {
        "form": PostForm(),
        "body": body
    })