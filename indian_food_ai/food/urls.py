from django.urls import path
from .views import PredictAPI, home
urlpatterns = [
    path('', home),
    path('predict/', PredictAPI.as_view()),

    ]