from django.urls import path
from .views import SuggestAPI
urlpatterns = [path('recipes/', SuggestAPI.as_view())]