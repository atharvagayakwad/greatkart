from django import forms

from store.models import ReviewRatingModel

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRatingModel 
        fields = ['subject', 'review', 'rating']