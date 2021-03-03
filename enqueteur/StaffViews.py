from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as dj_login
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import json
from django.core.serializers.json import DjangoJSONEncoder

from bs4 import BeautifulSoup
# Create your views here.
#Views de l'Enqueteur

def indexEnqueteur(request):
    return render(request, "EnqueteurPage/index-services.html")


def Trouvermission(request):
    return render(request, "EnqueteurPage/page-jobs-sidebar.html")


def mission_detail(request):
    return render(request, "EnqueteurPage/page-job-detail.html")


def apply_for_mission(request):
    return render(request, "EnqueteurPage/page-job-apply.html")


def mission(request):
    return render(request, "EnqueteurPage/page-blog-grid.html")


def account_messages(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-messages.html",{"enqueteur":enqueteur})


def account_payments(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-payments.html",{"enqueteur":enqueteur})


def account_profile(request):
    user = request.user
    enqueteur=Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-profile.html",{"enqueteur":enqueteur})


@login_required(login_url='login')
@csrf_exempt
def updateprofil(request):
    getprofildata = Enqueteur.objects.filter(user=request.user).values()
    if getprofildata:
        print('ok we got data of user')
        profildatajson = json.dumps(getprofildata[0], sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        if request.method == 'POST':
            if request.POST.get('senddata'):
                data = request.POST.get('senddata')
                data_dict = json.loads(data)
                print('data dict after update is :....')
                print(data_dict)
                Enqueteur.objects.filter(user=request.user).update(telephone=data_dict['telephone'],
                                                                   email=data_dict['email'],
                                                                   adresse=data_dict['adresse'])
                print('data saved and updated.....')
        else:
            print('noooooo data gotten')
    else:
        print('not data existing')
    return render(request, 'EnqueteurPage/account-setting.html', {'data': profildatajson, 'dataprofil': getprofildata[0]})



def account_works(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-works.html",{"enqueteur":enqueteur})

def contact_enqueteur(request):
    return render(request, "EnqueteurPage/page-contact-one.html")

def questionnaire(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        birth_day = request.POST.get('birth_day')
        genre = request.POST.get('genre')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        ordinateur= request.POST.get('ordinateur')
        vehicule= request.POST.get('vehicule')
        userexpen = request.POST.get('userexpen')
        userexp = request.POST.get('userexp')
        expmois = request.POST.get('expmois')
        societe = request.POST.get('societe')
        lunettes = request.POST.get('lunettes')
        logement = request.POST.get('logement')
        habitation = request.POST.get('habitation')
        langues = request.POST.get('langues')
        meilleur = request.POST.get('meilleur')
        pire = request.POST.get('pire')
        restaurant = request.POST.get('restaurant')
        situation = request.POST.get('situation')
        joindre = request.POST.get('joindre')
        enfants = request.POST.get('enfants')

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        created_at = datetime.datetime.now()
        email =request.user.email

        status = True
        user = request.user
        enqueteur = Enqueteur.objects.create(user=user,
                                             nom=nom,
                                             profile_pic=profile_pic,
                                             email=email,
                                             created_at=created_at,
                                             adresse=adresse,
                                             latitude=latitude,
                                             ordinateur=ordinateur,
                                             vehicule=vehicule,
                                             longitude=longitude,
                                             birth_day=birth_day,
                                             telephone=telephone,
                                             userexpen=userexpen,
                                             userexp=userexp,
                                             expmois=expmois,
                                             societe=societe,
                                             lunettes=lunettes,
                                             logement=logement,
                                             habitation=habitation,
                                             langues=langues,
                                             meilleur=meilleur,
                                             pire=pire,
                                             restaurant=restaurant,
                                             joindre=joindre,
                                             situation=situation,
                                             genre=genre,
                                             enfants=enfants,
                                             status=status
                                             )
        enqueteur.profile_pic = profile_pic_url
        enqueteur.save()
        return redirect('indexEnqueteur')

    return render(request, 'questionnaire.html')
