from django.urls import path, include
from . import views

urlpatterns = [
    path('live/',views.index,name='live-stream' ),
    path('facecam_feed/', views.facecam_feed, name='facecam_feed'),
    path('displayvideo/', views.displayvideo, name='displayvideo'),
    path('displayusers/', views.displayusers, name='displayusers'),
]