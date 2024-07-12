from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from .forms import RestaurantForm
from django.views.decorators.http import require_http_methods


from restaurant_review.models import Restaurant, Review

# Create your views here.

def index(request):
    print('Request for index page received')
    restaurants = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).annotate(review_count=Count('review'))
    lastViewedRestaurant = request.session.get("lastViewedRestaurant", False)
    return render(request, 'restaurant_review/index.html', {'LastViewedRestaurant': lastViewedRestaurant, 'restaurants': restaurants})


def details(request, id):
    print('Request for restaurant details page received')
    restaurant = get_object_or_404(Restaurant, pk=id)
    request.session["lastViewedRestaurant"] = restaurant.name
    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant})


def create_restaurant(request):
    print('Request for add restaurant page received')
    return render(request, 'restaurant_review/create_restaurant.html')


@csrf_exempt
def add_restaurant(request):
    try:
        name = request.POST['restaurant_name']
        street_address = request.POST['street_address']
        description = request.POST['description']
    except (KeyError):
        # Redisplay the form
        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.street_address = street_address
        restaurant.description = description
        Restaurant.save(restaurant)

        return HttpResponseRedirect(reverse('details', args=(restaurant.id,)))


@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        # Redisplay the form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        Review.save(review)

    return HttpResponseRedirect(reverse('details', args=(id,)))

def delete_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    restaurant.delete()
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def update_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('details', args=(restaurant.id,)))
        else:
            return render(request, 'restaurant_review/update_restaurant.html', {'form': form})
    else:
        form = RestaurantForm(instance=restaurant)
        return render(request, 'restaurant_review/update_restaurant.html', {'form': form})
    

def delete_review(request, id):
    review = get_object_or_404(Review, pk=id)
    restaurant_id = review.restaurant.id
    review.delete()
    return HttpResponseRedirect(reverse('details', args=(restaurant_id,)))