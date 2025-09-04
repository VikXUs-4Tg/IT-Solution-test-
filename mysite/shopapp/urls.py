from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote_view, name='index'),
    path('add_new_quote/', views.add_new_quote, name='add_new_quote'),
    path('popular-quotes/', views.popular_quotes, name='popular_quotes'),
]