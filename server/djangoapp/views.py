from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_dealerid, get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
--- finished work!

# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
     return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
     return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://be43dd7c.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.address for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"] = dealerships
    return (render(request, 'djangoapp/index.html', context))
    

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
   
    if request.method == "GET":
        context = {}

        url = "https://be43dd7c.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        
        dealer = get_dealer_by_dealerid(url,dealer_id)
        context["dealer"]=dealer
        
        url = "https://be43dd7c.eu-gb.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        
        context["reviews"]=reviews
       
        #dealer_reviews = ' '.join([revi.review for revi in reviews])
       
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
#check if user authenticated
      user = request.user
      context = {}
      url = "https://be43dd7c.eu-gb.apigw.appdomain.cloud/api/dealership"
      dealer = get_dealer_by_dealerid(url,dealer_id)
      context["dealer"]=dealer
      
      if user:
        if request.method == "GET":
         

          cars=CarModel.objects.all
          context["cars"]=cars
         
          return render(request, 'djangoapp/add_review.html', context)
        else:
          url = "https://be43dd7c.eu-gb.apigw.appdomain.cloud/api/review"

          car = CarModel.objects.get(pk=request.POST["car"])
          review = {}
          review["name"]=request.user.username
          review["another"]=""
          review["car_make"]=car.make.name
          review["car_model"]=car.name
          review["car_year"]=int(car.year.strftime("%Y"))
          review["dealership"]=dealer_id
          review["id"]=dealer_id
          review["purchase"]= (request.POST["purchasecheck"] == 'on')
          review["purchase_date"]=request.POST["purchasedate"]
          review["review"]=request.POST["content"]
          review["time"] = datetime.utcnow().isoformat()
          json_payload = {}
          json_payload["review"]=review
          post_request(url, json_payload, dealerId=dealer_id)
          return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
      else:
          return redirect("djangoapp:dealer_details", dealer_id=dealer_id) 
