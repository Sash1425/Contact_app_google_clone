from django.urls import path, include
from .views import ContactDetailsView, SpamView, ContactSearchView

urlpatterns = [
    path('', ContactDetailsView.as_view()),
    path('spam/', SpamView.as_view()),
    path('search/', ContactSearchView.as_view())
]
