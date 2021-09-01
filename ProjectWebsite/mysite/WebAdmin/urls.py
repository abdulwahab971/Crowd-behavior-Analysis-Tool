from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home ),
    path('home/', views.home, name='WebAdmin-home'),
    path('livestream/', views.livestream, name='WebAdmin-livestream'),
    path('services/', views.services, name='WebAdmin-services'),
    path('contactus/', views.contactus, name='WebAdmin-contactus'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]
