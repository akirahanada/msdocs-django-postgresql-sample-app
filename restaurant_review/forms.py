# forms.py

from django import forms
from .models import Restaurant, Review

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'street_address', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'review_text', 'review_date']
