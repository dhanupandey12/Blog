from django import forms
from .models import reviewsData,reportPost,Comments


class ReviewDataForm(forms.ModelForm):
    class Meta():
        model = reviewsData
        fields = ['review',]

class ReportPostForm(forms.ModelForm):
    class Meta():
        model = reportPost
        fields = ['note',]