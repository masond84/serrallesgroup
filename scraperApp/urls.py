from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape_view, name="scrape_view"),
    path('', views.index_view, name="index_view"),
]