# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from . import restapis
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request) # Terminate user session
    data = {"userName":""} # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    
    try:
        # Check if user already exists
        User.objects.get(username=username)
        data = {"userName": username, "error": "Already Registered"}
    except User.DoesNotExist:
        # Create user
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Get cars view
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# Update the `get_dealerships` view to render the index page with
# a list of dealerships
# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealers_by_state(request, state):
    try:
        dealers = get_request(f"/fetchDealers/{state}")
        return JsonResponse({"status": 200, "dealers": dealers})
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})

def get_dealer_by_id(request, dealer_id):
    try:
        dealer = restapis.get_request(f"/fetchDealer/{dealer_id}")
        return JsonResponse({"status": 200, "dealer": dealer})
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})

def get_dealer_details(request, dealer_id):
    try:
        dealer = get_request(f"/fetchDealer/{dealer_id}")
        return JsonResponse({"status": 200, "dealer": dealer})
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})

def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
        if reviews:
            # Add sentiment analysis to each review
            for review in reviews:
                if 'review' in review:
                    sentiment_result = analyze_review_sentiments(review['review'])
                    if isinstance(sentiment_result, dict):
                        review['sentiment'] = sentiment_result.get('sentiment', 'neutral')
                    else:
                        review['sentiment'] = sentiment_result
            return JsonResponse({"status": 200, "reviews": reviews})
        else:
            return JsonResponse({"status": 200, "reviews": []})
    except Exception as e:
        return JsonResponse({"status": 200, "reviews": []})

@csrf_exempt
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            # Add sentiment analysis before posting review
            review_text = data.get('review', '')
            sentiment_result = analyze_review_sentiments(review_text)
            if isinstance(sentiment_result, dict):
                data['sentiment'] = sentiment_result.get('sentiment', 'neutral')
            else:
                data['sentiment'] = sentiment_result
            
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
