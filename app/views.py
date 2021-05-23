
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import UserModel,Train,Booking
from django.contrib.auth import logout
from .utils import id_creator
from .tasks import *
from celery import chain
import datetime

# Create your views here.
def home(request):
    #if the session is stored already
    if 'username' in request.session:
        # print(f"this is the key {request.session.username}")
        # print(total.get())
        return redirect("profile")
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user1 = UserModel.objects.get(email__exact=email)
                if password == user1.password:
                    # print("password is {} and entered is {}".format(user1.password, password))
                    request.session['username'] = user1.name
                    request.session['email'] = user1.email
                    messages.info(request, "User Login Successful!")
                    return redirect("profile")

            except:
                messages.info(request, "No such user!")

    return render(request, 'home.html', {})

# def home(request):
#     # if request.user.is_authenticated:
#     #     return redirect("profile")
#     # else:
#     #     if request.method=="POST":
#     #         email=request.POST.get("email")
#     #         password=request.POST.get("password")
#     #         user1=User.objects.get(email__exact=email)
#     #         print(f"your email and password are {user1.username} and {user1.email}")
#     #         if user1.check_password(password):
#     #             print(f"You are Authenticated {user1.username}")
#     #             messages.info(request,f"Successfully logged in as {user1.id}")
#     #             # user_loggedin=LoginSession.objects.filter(email__exact=email).first()
#     #             # if user_loggedin:
#     #             #     LoginSession.objects.filter(email__exact=email).update(lastlogin=datetime.datetime.now())
#     #             # else:
#     #             #     login_session_object=LoginSession(userid=user.id,email=user.email,lastlogin=datetime.datetime.now())
#     #             #     login_session_object.save()
#     #             return redirect("profile")
#     #             # return HttpResponseRedirect(reverse('profile'),args=["abc","email"])
#     #         else:
#     #             messages.info(request, "kindly check your credentials {}".format(request.POST.get("email")))
#
#     return render(request, 'home.html', {})


def profile(request):
    # forcing the user to login before using the profile
    if 'username' in request.session and request.session["username"]!=None:
        trains_available=Train.objects.filter(availibility=True)
        booking_created=Booking.objects.filter(email=request.session["email"])
        # print(booking_created)
        context={}
        context["trains_available"]=trains_available
        context["booking_created"]=booking_created
        if request.method=="POST":
            username=request.session["username"]
            email=request.session["email"]
            date=request.POST["date"]
            time=request.POST["time"]
            source=request.POST["source"]
            destination=request.POST["destination"]
            passengers=request.POST["number"]


            # print(request.POST)
            booking_details=Booking(username=username,date=date+" "+time,
                    source=source,destination=destination,passengers=passengers,email=email)
            booking_details.save()
            # print(str(booking_details.id)+"is the id after svaing")

            #celery tasks
            # status=check_train(source,destination)
            temp=date + " " + time
            check_train.apply_async(kwargs={"source":source,'destination':destination,"date":temp,
                                            "passengers":int(passengers),"id_train":booking_details.id})
            # status_booking=chain(check_status.si(date + " " + time),check_seats.si(int(passengers),status[0]))()
            # update_booking_status(status_booking.get(0),status_booking.get(1),booking_details.id,status[1],status[2])
            # status_booking.get()
            messages.info(request,"Booking successfully created!")
            return render (request,"loginlanding.html",context=context)


        return render(request,"loginlanding.html",context=context)
    else:
        return redirect("home")


def logout_fun(request):
    logout(request)
    messages.info(request, "You are logged out!")
    return redirect("home")


def register(request):
    if request.method=="POST":

        email = request.POST.get("email")
        name = request.POST.get("name")

        password = request.POST.get("password")

        user_object=UserModel(name=name,email=email,password=password,userid=id_creator(name))
        user_object.save()

        messages.info(request,"You are successfully registered!")
    return render(request,"register.html",{})