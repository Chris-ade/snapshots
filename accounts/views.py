from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from feed.models import *
from .forms import *

def register(request):
    '''
    Displays the account registration page if there is no account currently logged on also registers an account if the request method is POST.

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template displaying information about the specified user, or a 404 error page if the user does not exist.

    Example:
        GET /register/
    '''
    # Checks if user is logged in
    if request.user.is_authenticated:
        # Redirects to the home page
        return redirect(reverse('feed:home'))
    else:
        # Checks if request method is POST
        if request.method == 'POST':
              # Initialize the sign up form
              form = signup_form(request.POST)
              # Checks if the submitted form data is valid
              if form.is_valid():
                  username = form.cleaned_data['username']
                  email = form.cleaned_data['email']
                  password = form.cleaned_data['password']
                  cpassword = form.cleaned_data['cpassword']
                  # Checks if both passwords match
                  if password == cpassword:
                      # Checks if an account with the email already exists
                      if User.objects.filter(email=email).exists():
                          # Creates a message
                          messages.info(request, 'An account with that e-mail already exists')
                          # Redirects back to the sign up page with the message
                          return redirect(reverse('accounts:register'))
                      # Checks if an account with the username already exists
                      elif User.objects.filter(username=username).exists():
                          # Creates a message
                          messages.info(request, 'The username has been taken, try another')
                          # Redirects back to the sign up page with the message
                          return redirect(reverse('accounts:register'))
                      else:
                          # Creates an account with the credentials
                          user = User.objects.create_user(username=username, email=email, password=password)
                          # Save the account
                          user.save()
                          # Authenticates the user with the credentials
                          user_login = auth.authenticate(username=username, password=password)
                          # Logs the user in
                          auth.login(request, user_login)
                          # Redirects to the home page
                          return redirect(reverse('feed:home'))
                  else:
                      # Creates an error message
                      messages.info(request, 'The passwords does not match')
                      # Redirects back to the sign up page with the error
                      return redirect(reverse('accounts:register'))
              else:
                  # Creates an error message
                  messages.info(request, 'An error occurred!')
                  # Redirects back to the sign up page with the error
                  return redirect(reverse('accounts:register'))
        # Renders the sign up page
        return render(request, 'welcome/register.html', {'page_title': "Sign Up - SnapShots", 'form': signup_form()})

def login(request):
    '''
    Displays the user login page if there is no account currently logged.

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template of the login page.

    Example:
        GET /login/
    '''
    # Checks if user is logged in
    if request.user.is_authenticated:
        # Redirects to the home page
        return redirect(reverse('feed:home'))
    else:
      # Checks if request method is POST
      if request.method == 'POST':
          # Initialize the login form
          form = login_form(request.POST)
          # Checks if the submitted form data is valid
          if form.is_valid():
              username = form.cleaned_data['username']
              password = form.cleaned_data['password']
              # Authenticates the account credentials
              user = auth.authenticate(username=username, password=password)
              # Checks if authentication is successful
              if user:
                  # Logs in the account
                  auth.login(request, user)
                  # Redirects to the home page
                  return redirect(reverse('feed:home'))
              else:
                  # Initializes the login form with an initial value
                  form = login_form(initial={'username': username, 'password': password})
                  # Renders the login page with the error message and the initial form data
                  return render(request, 'welcome/login.html', {'page_title': "Snapshots - Exciting image sharing experience", 'form': form, 'error': 'Invalid credentials'})
          else:
              # Renders the login page with the error message and the initial form data
              return render(request, 'welcome/login.html', {'page_title': "Snapshots - Exciting image sharing experience", 'form': login_form(), 'error': 'An error occurred!'})
      else:
          # Initialize the login form
          form = login_form()
          # Renders the login page
          return render(request, 'welcome/login.html', {'page_title': "Snapshots - Exciting image sharing experience", 'form': form})

def terms(request):
    '''
    Renders the terms and conditions page

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template of the terms and conditions page.

    Example:
        GET /terms/
    '''
    return render(request, 'welcome/terms.html')

def privacy_policy(request):
    '''
    Renders the privacy policy page

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template of the privacy policy page.

    Example:
        GET /privacy/
    '''
    return render(request, 'welcome/privacy-policy.html')

@login_required
def logout(request):
    '''
    Logs out an account

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template of the login page on completion of the logout process.

    Example:
        GET /logout/
    '''
    # Checks if user is authenticated
    if request.user.is_authenticated:
        # Destroys the user session
        auth.logout(request)
        # response = HttpResponse()
        # response['HX-Redirect'] = reverse("accounts:login")
    # Redirects to the login page
    return redirect(reverse('accounts:login'))

@login_required
def profile(request, username):
  '''
    Retrieve information about a user.

    Args:
        request (object): the HTTP request object
        username: (string): the username of the user to be retrieved

    Returns:
        A rendered template displaying information about the specified user, or a 404 error page if the user does not exist.
    Example:
        GET /user/johndoe/
  '''
  try:
      user = User.objects.get(username=username)
      posts = Media.objects.filter(user__username=username)
      comments_count = Comments.objects.filter(user__username=username).count()
      context = {
        'page_title': f'@{user.username} - User on SnapShots',
        'user': user,
        'posts': posts,
        'post_count': posts.count(),
        'comments_count': comments_count,
      }
      return render(request, 'profile/content.html', context)
  except User.DoesNotExist:
      return render(request, 'errors/404.html')

@login_required
def feeds(request, username):
    '''
    Displays all the posts created by a user.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose posts are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the posts created by the user. If the user does not exist, returns a "404 Not Found" response.

    Example:
        GET /user/johndoe/feeds/
    '''
    try:
        user_obj = User.objects.get(username=username)
        media_obj = Media.objects.filter(user__username=username)
        context = {
          'posts': media_obj,
          'user': user_obj
        }
        return render(request, 'profile/feeds.html', context)
    except User.DoesNotExist:
        return HttpResponse("Not Found", status=404)

@login_required
def comments(request, username):
    '''
    Displays all the comments created by a user.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose comments are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the comments created by the user. If the user does not exist, returns a "404" page.

    Example:
        GET /user/johndoe/comments/
    '''
    try:
        user_obj = User.objects.get(username=username)
        comments_obj = Comments.objects.filter(user__username=username).distinct()
        context = {
          'comments': comments_obj,
          'user': user_obj
        }
        return render(request, 'profile/comments.html', context)
    except User.DoesNotExist:
        return HttpResponse("Not Found", status=404)

@login_required
def images(request, username):
    '''
    Displays all the posts with images created by a user.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose feeds are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the posts created by the user. If the user does not exist, returns a "404" page.

    Example:
        GET /user/johndoe/images/
    '''
    try:
        user_obj = User.objects.get(username=username)
        media_obj = Media.objects.filter(user__username=username, files__isnull=False, files__type='image').distinct().prefetch_related('files')
        context = {
          'posts': media_obj,
          'user': user_obj
        }
        return render(request, 'profile/images.html', context)
    except User.DoesNotExist:
        return HttpResponse("Not Found", status=404)

@login_required
def videos(request, username):
    '''
    Displays all the posts with videos created by a user.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose feeds are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the posts created by the user. If the user does not exist, returns a "404 Not Found" response.

    Example:
        GET /user/johndoe/videos/
    '''
    try:
        user_obj = User.objects.get(username=username)
        media_obj = Media.objects.filter(user__username=username, files__isnull=False, files__type='video').distinct().prefetch_related('files')
        context = {
          'posts': media_obj,
          'user': user_obj
        }
        return render(request, 'profile/videos.html', context)
    except User.DoesNotExist:
        return HttpResponse("Not Found", status=404)
