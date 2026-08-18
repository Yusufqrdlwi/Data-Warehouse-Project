from django.urls import path
from . import views

urlpatterns = [
    path('transactions_seeder/', views.get_posts, name='get-posts'),
]