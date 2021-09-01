from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request,'WebAdmin/home.html')

@login_required
def livestream(request):

    return render(request,'WebAdmin/live_stream.html')

@login_required
def services(request):
    return render(request,'WebAdmin/services.html')

@login_required
def contactus(request):
    return render(request,'WebAdmin/contactus.html')