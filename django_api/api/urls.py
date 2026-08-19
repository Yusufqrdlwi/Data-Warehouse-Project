from django.urls import path
from . import views

urlpatterns = [
    #path('transactions_seeder/', views.get_posts, name='get-posts'),
    path('sync_posts/', views.fetch_and_save_live_posts, name='sync-posts'),
]