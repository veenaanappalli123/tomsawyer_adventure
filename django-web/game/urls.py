from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('story/<int:story_id>/', views.play_story, name='play_story'),
    path('stats/', views.stats, name='stats'),

]
