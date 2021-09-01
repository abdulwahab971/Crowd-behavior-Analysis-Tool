from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponse
import beepy as bp
from .detect_video import Model
import os,datetime

from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
import glob
# Create your views here.
Program_status = False

def displayusers(request):
    User = get_user_model()
    users = User.objects.all()
    context={
        "users": users
    }


    return render(request, 'streamapp/displayusers.html', context)




@login_required
def displayvideo(request):

    list= []

    data = request.POST.get('dateHTML')
    data = str(data)
    data = data.split(':')[0]

    submitbutton = request.POST.get('Submit')
    if submitbutton =='Submit':

        for filepath in glob.iglob(
                os.path.join(settings.BASE_DIR, r'streamapp\static\streamapp/*.mp4')):

            t = os.path.getmtime(filepath)
            x = str(datetime.datetime.fromtimestamp(t).date())
            if data == x:

                filepath = filepath.replace(
                     os.path.join(settings.BASE_DIR, "streamapp\\static\\"), "/")
                filepath = filepath.replace("\\", "/")
                list.append(filepath)

    else:
    #gets the path of all the videos in the folder and changes them into static address to use them in HTML
        for filepath in glob.iglob(
                os.path.join(settings.BASE_DIR,
                             r'streamapp\static\streamapp/*.mp4')):
            filepath = filepath.replace(
                 os.path.join(settings.BASE_DIR, "streamapp\\static\\"), "/")
            filepath = filepath.replace("\\", "/")

            list.append(str(filepath))
        #display by date
    context = {
        "address": list,
        "datepython": data,
        "submitbutton": submitbutton
    }


    return render(request,'streamapp/DisplayVideo.html',context)




def index(request):
    f = open(os.path.join(settings.BASE_DIR, "streamapp/figting.txt"),
             "a")
    f.truncate(0)
    f.close()
    i=1
    while True:
        f = open( os.path.join(settings.BASE_DIR, "streamapp/figting.txt"),
                 "r")
        read = str(f.readline())

        context = {
            'read':read

        }
        i=i+1
        return render(request, 'streamapp/camera.html', context)




def gen(detect_video):

    while True:
        frame, b = detect_video.get_frame()
        # 0 is for fight
        if b == 0:
            bp.beep(8)
        elif b == 1:
            bp.beep(1)




        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')




def facecam_feed(request):
    #for live video stream
    return StreamingHttpResponse(gen(Model()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

