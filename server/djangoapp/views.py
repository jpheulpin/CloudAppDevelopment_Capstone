from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_from_cf_by_id, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
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
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/0384c197-cd86-4d69-b71d-8725c6b46bbf/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context = {}
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url_reviews = "https://eu-gb.functions.appdomain.cloud/api/v1/web/0384c197-cd86-4d69-b71d-8725c6b46bbf/dealership-package/get-review"
        url_dealer = "https://eu-gb.functions.appdomain.cloud/api/v1/web/0384c197-cd86-4d69-b71d-8725c6b46bbf/dealership-package/get-dealership"
        reviews = get_dealer_reviews_from_cf(url_reviews, dealerId=dealer_id)
        context = {}
        context['reviews'] = reviews
        context['dealer'] = get_dealer_from_cf_by_id(url_dealer,  dealer_id=dealer_id)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/0384c197-cd86-4d69-b71d-8725c6b46bbf/dealership-package/get-dealership"
        dealer = get_dealer_from_cf_by_id(url, dealer_id)
        cars = CarModel.objects.filter(DealerId=dealer_id)
        context["cars"] = cars
        context["dealer"] = dealer
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == "POST":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/0384c197-cd86-4d69-b71d-8725c6b46bbf/dealership-package/post-review"
        review = {}
        review["id"] = 1
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']
        review["car_make"] = "Audi"
        review["car_model"] = "Car"
        review["car_year"] = 2021
        review["name"] = "John"
        review["purchase"] = True
        review["purchase_date"] = request.POST['purchasedate']
        json_payload = {}
        json_payload["review"] = review
        response = post_request(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)