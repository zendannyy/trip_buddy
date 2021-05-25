from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from django.db.models import Q
from .models import *


def index(request):
    return render(request, "index.html")


def login(request):
    print(request.POST)
    request.session['check'] = "logged_in"
    request.session['luname'] = request.POST['l_uname']
    errors = Users.objects.loginvalidator(request.POST, request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    request.session.clear()
    loginuser = Users.objects.get(username=request.POST['l_uname'].lower())
    request.session['login_id'] = loginuser.id
    return redirect("/travels")


def register(request):
    print(request.POST)
    request.session['check'] = "registered"
    request.session['name'] = request.POST['r_name']
    request.session['uname'] = request.POST['r_uname']
    errors = Users.objects.registervalidator(request.POST, request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    request.session.clear()
    regis_user = request.POST['r_uname'].lower()
    password = request.POST['r_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuser = Users.objects.create(name=request.POST['r_name'], username=regis_user, password=pw_hash)
    request.session['login_id'] = newuser.id
    print(request.session['login_id'])
    return redirect("/")


def travels(request):
    userid = Users.objects.get(id=request.session['login_id'])
    context = {
        'user': Users.objects.get(id=request.session['login_id']),
        'your_trip': Trips.objects.filter(Q(user=userid) | Q(favoriter=userid)).distinct(),
        'other_trip': Trips.objects.exclude(Q(user=userid) | Q(favoriter=userid)).distinct(),
    }
    return render(request, "travels.html", context)


def jointrip(request, tripid):
    user = Users.objects.get(id = request.session['login_id'])
    trip = Trips.objects.get(id = tripid)
    trip.favoriter.add(user)
    return redirect("/travels")


def unjointrip(request, tripid):
    user = Users.objects.get(id = request.session['login_id'])
    trip = Trips.objects.get(id = tripid)
    trip.favoriter.remove(user)
    return redirect("/travels")


def addtravel(request):
    """add travel plans"""
    return render(request, "addtravel.html")


def recordtravel(request):
    print(request.POST)
    request.session['dest'] = request.POST['dest']
    request.session['desc'] = request.POST['desc']
    request.session['datefrom'] = request.POST['datefrom']
    request.session['dateto'] = request.POST['dateto']
    errors = Trips.objects.recordvalidator(request.POST, request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/travels/add")
    userid = Users.objects.get(id=request.session['login_id'])
    Trips.objects.create(destination=request.POST['dest'], description=request.POST['desc'], datefrom=request.POST['datefrom'], dateto=request.POST['dateto'], user=userid)
    request.session['dest'] = ""
    request.session['desc'] = ""
    request.session['datefrom'] = ""
    request.session['dateto'] = ""
    return redirect("/travels")


def destination(request, tripid):
    context = {
        'tripinfo': Trips.objects.get(id=tripid),
    }
    return render(request, "destination.html", context)


def delete(request, tripid):
    trip = Trips.objects.get(id=tripid)
    trip.delete()
    return redirect("/travels")


def logout(request):
    request.session.clear()
    return redirect("/")
