from django.urls import path, include
from .views import (RegistrationView, RegistartionSecondView, CardView, GetCardView, 
                    UseCardView, GetCurrentCardView, GetHistoryView, AddPurchase)

urlpatterns = [
    path('enterAccount', RegistrationView.as_view()),
    path('getCards', GetCardView.as_view()),
    path('useCard', UseCardView.as_view()),
    path('getCurrentCard', GetCurrentCardView.as_view()),
    path('getHistory', GetHistoryView.as_view()),
    path('addPurchase', AddPurchase.as_view()),

    path('registration/', RegistartionSecondView.as_view()),
    path('card/', CardView.as_view())
]