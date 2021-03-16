from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from .decorators import admin_only
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
import os
import codecs
# Create your views here.
from django.core.paginator import Paginator

data = {}
indice = 0
mlist = []
filtredNone = []
averge_list = []

jdata = {}


#Views de l'Enqueteur

def text(request):
    return render(request, "new/index-customer.html")

def indexEnqueteur(request):
    return render(request, "EnqueteurPage/index-services.html")

@login_required
def article1(request):
    return render(request, "EnqueteurPage/page-blog-detail-two.html")

@login_required
def article2(request):
    return render(request, "EnqueteurPage/page-blog-detail-twoo.html")

@login_required
def article3(request):
    return render(request, "EnqueteurPage/page-blog-detail-two3.html")

@login_required
def article4(request):
    return render(request, "EnqueteurPage/page-blog-detail-two4.html")

@login_required
def article5(request):
    return render(request, "EnqueteurPage/page-blog-detail-two5.html")
# views des missions enqueteurs : trouver une mission voir les missions

@login_required
def Trouvermission(request):
    post = Mission.objects.all()
    message_paginator = Paginator(post, 6)
    page_num = request.GET.get('page')
    page = message_paginator.get_page(page_num)
    context = {
        'count': message_paginator.count,
        'page': page,
        'post': post,
    }
    return render(request, "EnqueteurPage/page-jobs-sidebar.html",context)


@login_required
def mission(request):
    servey=SurveyData.objects.filter(user=request.user.id).first()
    candidature = Candidature.objects.all()
    print(candidature)
    context = {
        'servey': servey,
        'candidature':candidature
    }
    return render(request, "EnqueteurPage/page-blog-grid.html", context)


@login_required
def mission_detail(request,post_id):
    post=Mission.objects.get(id=post_id)
    candidature=Candidature.objects.filter(enqueteur_id=request.user.id).first()


    context = {
        'post': post,
        'candidature': candidature,
    }
    return render(request, "EnqueteurPage/page-job-detail.html",context)


#candidature

@login_required
def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("apply_for_mission"))
    else:
        staff_obj=Enqueteur.objects.get(user=request.user)
        mission_id = request.POST.get("mission_id")

        motivation=request.POST.get("motivation")

        try:
            mission_obj = Mission.objects.get(id=mission_id)
            leave_report=Candidature(enqueteur_id=staff_obj,mission_id=mission_obj,motivation=motivation,candidature_status=0)


            leave_report.save()
            messages.success(request, "Parfait, votre candidature est transmise a notre service relation pour la verification, vous reseverez une reponse dans votre boite mail")
            return HttpResponseRedirect(reverse("mission_detail",kwargs={"post_id":mission_id}))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("mission_detail",kwargs={"post_id":mission_id}))

# validation des candidatures


@login_required
def apply_for_mission(request,mission_id):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    mission=Mission.objects.get(id=mission_id)
    return render(request, "EnqueteurPage/page-job-apply.html",{"enqueteur":enqueteur,'mission':mission})

@admin_only
def staff_leave_view(request):
    #leaves=Candidature.objects.all()
    leaves = Candidature.objects.get_queryset().order_by('-created_at')
    message_paginator = Paginator(leaves, 5)
    page_num = request.GET.get('page')
    page = message_paginator.get_page(page_num)
    context = {
        'count': message_paginator.count,
        'page': page,
        'leaves': leaves,
    }
    return render(request,"administrateur/staff_leave_view.html",context)

@admin_only
def staff_approve_leave(request,leave_id):
    leave=Candidature.objects.get(id=leave_id)
    leave.candidature_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

@admin_only
def staff_disapprove_leave(request,leave_id):
    leave=Candidature.objects.get(id=leave_id)
    leave.candidature_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


@login_required
def account_messages(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user.id)
    message= Contact_admin.objects.get_queryset().filter(enqueteur_id=enqueteur.id).order_by('-created_at')
    message_paginator = Paginator(message, 5)
    page_num = request.GET.get('page')
    page = message_paginator.get_page(page_num)
    context = {
            'count': message_paginator.count,
            'page': page,
        'message':message,
        'enqueteur':enqueteur
        }
    return render(request, "EnqueteurPage/account-messages.html",context)


@login_required
def account_payments(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-payments.html",{"enqueteur":enqueteur})

@admin_only
def builder(request):

    return render(request, "index.html")


@login_required
def account_profile(request):


    try:
        user = request.user
        enqueteur=Enqueteur.objects.get(user=user)
        post = Actualite.objects.all()
        message_paginator = Paginator(post, 4)
        page_num = request.GET.get('page')
        page = message_paginator.get_page(page_num)
        context = {
            'count': message_paginator.count,
            'page': page,
            'post': post,
            'enqueteur':enqueteur,
        }
    except Enqueteur.DoesNotExist:
        return redirect('questionnaire')
    return render(request, "EnqueteurPage/account-profile.html",context)

@login_required
@csrf_exempt
def updateprofil(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("apply_for_mission"))
    else:
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')

        enqueteur_id = request.user.id

        try:
            leave_report = Enqueteur.objects.get(id=enqueteur_id)
            leave_report.telephone=telephone
            leave_report.adresse=adresse
            leave_report.email=email
            leave_report.save()
            messages.success(request,"Parfait, votre candidature est transmise a notre service relation pour la verification, vous reseverez une reponse dans votre boite mail")
            return HttpResponseRedirect('/account_settings')


       # profile_pic = request.FILES['profile_pic']
        #fs = FileSystemStorage()
        #filename = fs.save(profile_pic.name, profile_pic)
        #profile_pic_url = fs.url(filename)

            #return render(request, 'EnqueteurPage/account-setting.html',{'enqueteur':enqueteur})
        except:
            return render(request, "EnqueteurPage/account-setting.html", {"enqueteur": enqueteur})

@login_required
def account_settings(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-setting.html",{"enqueteur":enqueteur})


@login_required
def account_works(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-works.html",{"enqueteur":enqueteur})

@login_required
def contact_enqueteur(request):
    return render(request, "EnqueteurPage/page-contact-one.html")


#Views D'acceuil
def index(request):
    return render(request, "Homepage/index-services.html")

def service(request):
    return render(request, "Homepage/page-services.html")

def panel(request):
    return render(request, "Homepage/index-customer.html")

def auth_re_password(request):
    return render(request, "Homepage/auth-re-password.html")

def actualite(request):
    post = Actualite.objects.all()
    categorie = Categorie.objects.all()

    message_paginator = Paginator(post, 6)
    page_num = request.GET.get('page')
    page = message_paginator.get_page(page_num)
    context = {
        'count': message_paginator.count,
        'page': page,
        'post': post,
        'categorie':categorie,
    }
    return render(request, "Homepage/page-blog-list.html",context)

def actualite_detail(request,post_id):
    post=Actualite.objects.get(id=post_id)

    return render(request, "Homepage/page-blog-detail-two.html",{"post":post})

def faq(request):
    return render(request, "Homepage/helpcenter-faqs.html")



def contact(request):

    return render(request, "Homepage/page-contact-one.html")

@csrf_exempt
@login_required
def contact_sent_enqueteur(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user.id)
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        comments= request.POST.get('comments')
        try:
            contact = Contact_enqueteur.objects.create(enqueteur_id=enqueteur, comments=comments)
            contact.save()
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return HttpResponseRedirect('/account_messages')
        except:
            return HttpResponseRedirect('/account_messages')

#Contact Message
@csrf_exempt
def contact_sent(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        comments= request.POST.get('comments')
        try:
            contact = Contact.objects.create(name=name, email=email, subject="From contact form", comments=comments)
            contact.save()
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return HttpResponseRedirect('/contact')
        except:
            return HttpResponseRedirect('/contact')

#Register

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = createUser()
        if request.method == 'POST':
            form = createUser(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created {}'.format(username))
                return redirect('login')
        return render(request, 'Homepage/auth-signup-three.html', {'form': form})

#Validation des comptes :

@login_required
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

def login(request):
    if request.user.is_authenticated:
        return redirect('indexEnqueteur')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
                try:
                    currentuser = Enqueteur.objects.get(user=request.user)
                    print(currentuser)
                    if len(currentuser.nom) > 0:
                        return redirect('indexEnqueteur')
                    else:
                        print('something went wrong')
                except Enqueteur.DoesNotExist:
                    return redirect('questionnaire')
            else:
                messages.info(request, 'your password or username not correct')
                return render(request, 'Homepage/auth-login.html')
        return render(request, 'Homepage/auth-login.html')


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = createUser()
        if request.method == 'POST':
            form = createUser(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created {}'.format(user))
                return redirect('login')
        return render(request, 'register.html', {'form': form})


@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect('/login/')


#Administrateur Views
@admin_only
def indexAdmin(request):
    consultant_count1=Enqueteur.objects.all().count()
    mission_count=Mission.objects.all().count()

    context = {
        'consultant_count1': consultant_count1,
        'mission_count': mission_count
    }
    return render(request, "Administrateur/index.html",context)

@admin_only
def test(request):
    return render(request, "Administrateur/forms/general.html")


@admin_only
def IndexAdmin2(request):
    return render(request, "Administrateur/indexNew.html")


@admin_only
def gestion(request):
    return render(request, "Administrateur/gestion.html")

@admin_only
def tableau(request):
    surveydata = SurveyData.objects.all()
    retrivedata = SurveyData.objects.filter(user=request.user).values()
    json_list = []
    if retrivedata:
        for i in retrivedata:
            dict_data = json.loads(i['data'])
            dict_data['date'] = i.get('date')
            dict_data['nameform'] = i.get('nameform')
            dict_data['user'] = i.get('user')
            json_list.append(dict_data)
        headelement = json_list[0]
        print(dict_data)

    else:
        print('fffffffffffffffffffffffffffff')
    return render(request, "Administrateur/tables/data.html", {'surveydata': surveydata,'data': json_list, 'head': headelement.keys()})


#gestion des enqueteurs

@admin_only
def users_status(request):
    users=Enqueteur.objects.all()
    return render(request, "Administrateur/projects.html",{'users':users})


@admin_only
def profile(request,enqueteur_id):
    enqueteur=Enqueteur.objects.get(id=enqueteur_id)
    return render(request, "Administrateur/profile.html",{'enqueteur':enqueteur})

#Mappage des enqueteurs

@admin_only
def gpsmap(request):
    mls = []
    gps = Enqueteur.objects.all().values()
    print(len(gps))
    for i in range(len(gps)):
        mmdict = {}
        mmdict['latitude'] = gps[i]['latitude']
        mmdict['longitude'] = gps[i]['longitude']
        mmdict['nom'] = gps[i]['nom']
        mmdict['adresse'] = gps[i]['adresse']
        mls.append(mmdict)
        mlsjson = json.dumps(mls, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    print(mlsjson)
    return render(request, 'Administrateur/map.html', {'datamap': mlsjson})



#Affichage des resultats des missions

@admin_only
@csrf_exempt
def showdata(request):
    listmission = []
    json_list = []
    head = []
    retrieve_data = SurveyData.objects.all().values()
    for i in range(len(retrieve_data)):
        listmission.append(retrieve_data[i]['nameform'])
    mylist = list(dict.fromkeys(listmission))
    if request.method == 'POST':
        mission = request.POST.get('mission')
        retrivedata = SurveyData.objects.filter(nameform=mission).values()
        if retrivedata:
            for i in retrivedata:
                dict_data = json.loads(i['data'])
                dict_data['date'] = i.get('date')
                dict_data['nameform'] = i.get('nameform')
                dict_data['user'] = i.get('user')
                json_list.append(dict_data)
                headelement = json_list[0]
            for key, value in headelement.items():
                head.append(key)


        else:
            print('fffffffffffffffffffffffffffff')
            # {'data': json_list, 'head': headelement.keys()}
    return render(request, 'Administrateur/data.html', {'listmission': mylist, 'head': head, 'data': json_list})



@admin_only
def filterUserMission(request, user, mission):
    mlist = []
    mfilter = SurveyData.objects.filter(nameform=mission).filter(user=user).values()
    if mfilter:
        for i in range(len(mfilter)):
            jsontodict = json.loads(mfilter[i].get('data'))
            jsontodict['user'] = mfilter[i].get('user')
            jsontodict['mission'] = mfilter[i].get('nameform')
            jsontodict['date'] = mfilter[i].get('date')
            jsontodict['id'] = mfilter[i].get('id')
            mlist.append(jsontodict)
        headtable = mlist[0].keys()
    else:
        return redirect('login')
    return render(request, 'Administrateur/filtermissionuser.html', {'data': mlist, 'head': headtable})


#gestion des formulaires

@admin_only
def manage_forms(request):
    servey=CreateForms.objects.all()
    return render(request,"administrateur/gestion_forms.html",{"servey":servey})



@admin_only
def view_form(request,servey_id):
    servey=SurveyData.objects.get(id=servey_id)

    return render(request,"administrateur/edit_post.html",{"servey": servey})

@admin_only
def delete_form(request,servey_id):
    servey=CreateForms.objects.get(id=servey_id)
    servey.delete()
    return redirect("manage_forms")

#gestion des missions + organismes

@admin_only
def manage_mission(request):
    organisme=Organisme.objects.all()
    mission=Mission.objects.all()

    servey=CreateForms.objects.all()

    return render(request,"administrateur/manage_mission.html",{'organisme':organisme, "servey":servey, 'mission':mission})


@admin_only
def add_organisme_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:

        nom = request.POST.get("nom")
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        profile_pic_url = fs.url(filename)
        try:

            organisme=Organisme(nom=nom,photo=photo)
            organisme.profile_pic = profile_pic_url
            organisme.save()
            messages.success(request,"Successfully Added organisme")
            return HttpResponseRedirect(reverse("manage_mission"))
        except:
            messages.error(request,"Failed To Add organisme")
            return HttpResponseRedirect(reverse("manage_mission"))


@admin_only
def add_mission_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:

        ref = request.POST.get("ref")
        nom = request.POST.get("nom")
        organisme_id = request.POST.get("organisme")
        thematique = request.POST.get("thematique")
        quizz_id = request.POST.get("quizz")
        remuneration = request.POST.get("remuneration")
        description = request.POST.get("description")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        try:

            mission=Mission(ref=ref, nom=nom,thematique=thematique,remuneration=remuneration,description=description, date_debut=date_debut,date_fin=date_fin,ville=ville,pays=pays)
            quizz_obj = CreateForms.objects.get(id=quizz_id)
            mission.questionnaire = quizz_obj
            organisme_obj = Organisme.objects.get(id=organisme_id)
            mission.organisme = organisme_obj

            mission.save()
            messages.success(request,"Successfully Added mission")
            return HttpResponseRedirect(reverse("manage_mission"))
        except:
            messages.error(request,"Failed To Add mission")
            return HttpResponseRedirect(reverse("manage_mission"))


@admin_only
def edit_mission(request,mission_id):
    mission = Mission.objects.get(id=mission_id)
    organisme = Organisme.objects.all()
    servey = CreateForms.objects.all()
    return render(request,"administrateur/edit_mission.html",{'organisme':organisme, "servey":servey,"mission": mission})


@admin_only
def edit_mission_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        mission_id=request.POST.get("mission_id")
        ref = request.POST.get("ref")
        nom = request.POST.get("nom")
        organisme_id = request.POST.get("organisme")
        thematique = request.POST.get("thematique")
        quizz_id = request.POST.get("quizz")
        remuneration = request.POST.get("remuneration")
        description = request.POST.get("description")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        #try:

        mission = Mission.objects.get(id=mission_id)
        mission = Mission(ref=ref, nom=nom, thematique=thematique, remuneration=remuneration, description=description,date_debut=date_debut, ville=ville, pays=pays)
        mission.date_fin=date_fin
        quizz_obj = CreateForms.objects.get(id=quizz_id)
        mission.questionnaire = quizz_obj
        organisme_obj = Organisme.objects.get(id=organisme_id)
        mission.organisme = organisme_obj

        mission.save()
        #messages.success(request,"Successfully Edited mission")
        #    return HttpResponseRedirect(reverse("edit_mission",kwargs={"mission_id":mission_id}))
        #except:
         #   messages.error(request,"Failed To Edit mission")
          #  return HttpResponseRedirect(reverse("edit_mission",kwargs={"mission_id":mission_id}))


@admin_only
def delete_mission(request,mission_id):
    mission=Mission.objects.get(id=mission_id)
    mission.delete()
    return redirect("manage_mission")

#validation de la visite


@admin_only
def validation_visite(request):
    servey=SurveyData.objects.all()

    return render(request, "Administrateur/validation_visite.html",{"servey":servey})


@admin_only
def staff_approve_visite(request,survey_id):
    leave=CreateForms.objects.get(id=survey_id)
    leave.visite_status=1
    leave.save()
    return HttpResponseRedirect(reverse("validation_visite"))

@admin_only
def staff_disapprove_visite(request,survey_id):
    leave = CreateForms.objects.get(id=survey_id)
    leave.visite_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("validation_visite"))


#Gestion d'actualité

@admin_only
def add_post_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:

        title = request.POST.get("title")
        content = request.POST.get("content")
        keywords = request.POST.get("keywords")
        photo = request.POST.get("photo")

        try:

            actualite=Actualite(title=title, content=content,keywords=keywords,photo=photo)
            actualite.save()
            messages.success(request,"Successfully Added Post")
            return HttpResponseRedirect(reverse("manage_post"))
        except:
            messages.error(request,"Failed To Add Post")
            return HttpResponseRedirect(reverse("manage_post"))


@admin_only
def manage_post(request):
    post=Actualite.objects.all()
    return render(request,"administrateur/manage_post.html",{"post":post})


@admin_only
def edit_post(request,post_id):
    post = Actualite.objects.get(id=post_id)
    return render(request,"administrateur/edit_post.html",{"post": post})


@admin_only
def delete_post(request,post_id):
    post = Actualite.objects.get(id=post_id)
    post.delete()
    return redirect("manage_post")


@admin_only
def edit_post_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        post_id=request.POST.get("post_id")
        title=request.POST.get("title")
        content=request.POST.get("content")
        keywords=request.POST.get("keywords")

        try:
            post=Actualite.objects.get(id=post_id)
            post.title=title
            post.content=content
            post.keywords=keywords
            post.save()
            messages.success(request,"Successfully Edited post")
            return HttpResponseRedirect(reverse("edit_post",kwargs={"post_id":post_id}))
        except:
            messages.error(request,"Failed to Edit post")
            return HttpResponseRedirect(reverse("edit_post",kwargs={"post_id":post_id}))


#Serveyjs demo

@admin_only
def servey(request):
    return render(request, "Administrateur/servey.html")

#gestion des messages INBOX

@admin_only
def sent(request):
    return render(request, "Administrateur/mailbox/mail-sent.html")


@admin_only
def mailbox_compose(request):
    return render(request, "Administrateur/mailbox/compose.html")


@admin_only
def mailbox_compose_envoie(request,enqueteur_id):
    user = Enqueteur.objects.get(id=enqueteur_id)
    return render(request, "Administrateur/mailbox/compose.html",{'user':user})


@admin_only
def mailbox_compose_envoie_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:

        enqueteur_id=request.POST.get("enqueteur_id")
        reply=request.POST.get("reply")

        try:
            post=Contact_admin(reply=reply)
            quizz_obj = Enqueteur.objects.get(id=enqueteur_id)
            post.enqueteur_id = quizz_obj
            post.save()
            messages.success(request,"Le message est transmis avec succés ")
            return HttpResponseRedirect(reverse("profile", kwargs={"enqueteur_id": enqueteur_id}))
        except:
            messages.error(request,"Error 404")
            return render(request, "Administrateur/profile.html", {'enqueteur_id': enqueteur_id})


@admin_only
def mailbox(request):
    contact=Contact.objects.all()
    contact_enqueteur=Contact_enqueteur.objects.all()
    message_count=Contact.objects.all().count()
    message_countt=Contact_enqueteur.objects.all().count()
    me=message_count+message_countt
    return render(request, "Administrateur/mailbox/mailbox.html",{'contact':contact, 'contact_enqueteur':contact_enqueteur,'message_count':message_count,'me':me})

@admin_only
def mailbox_read_enqueteur(request,message_id):
    message= Contact_enqueteur.objects.get(id=message_id)
    return render(request, "Administrateur/mailbox/read-mail_enqueteur.html",{'message':message})

@admin_only
def mailbox_read_contact(request,contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, "Administrateur/mailbox/read-mail.html",{'contact':contact})

def terms(request):
    return render(request, "page-terms.html")



def missiontest(request):
    return render(request, "questionnairetest.html")


@admin_only
def getaverge(request, mission):
    data = []
    clust = []
    list_keys = []
    list_values = []
    final_dict = dict()
    try:
        if not avergedata.objects.filter(namemission=mission).exists():
            emptyaverge = avergedata.objects.create(namemission=mission, averges=json.dumps(jdata))
            emptyaverge.save()

        dataaverge = SurveyData.objects.filter(nameform=mission).values()
        for i in range(len(dataaverge)):
            data.append(json.loads(dataaverge[i].get('data')))
        if request.method == 'POST':
            table = request.POST.get('averge')
            if len(table) != 0:
                for i in range(len(data)):
                    for k, v in data[i].items():
                        keyslower = k.lower()
                        print(keyslower)
                        if keyslower.startswith(table):
                            clust.append(v)
                sum = 0
                for i in clust:
                    sum = sum + eval(i)
                final_dict[table] = sum / len(clust)
                averge_list.append(final_dict)
                print(len(averge_list))
                if len(averge_list) == 5:
                    jsonlist = json.dumps(averge_list)
                    avergedata.objects.filter(namemission=mission).update(averges=jsonlist)
                    averge_list.clear()
                getaverge = avergedata.objects.filter(namemission=mission).values()
                for i in getaverge:
                    avg = json.loads(i.get('averges'))
                    print(avg)
                    for c in avg:
                        for h in c.keys():
                            list_keys.append(h)

                        for g in c.values():
                            list_values.append(g)

            else:
                return HttpResponse('you have to fill a filed to get a valid averges')

    except IndexError:
        return HttpResponse('this url or mission dosnt exist...')
    return render(request, 'Administrateur/tables/averge.html', {'key': list_keys,
                                                                 'value': list_values,
                                                                 'jsonkey': json.dumps(list_keys),
                                                                 'jsonvalue': json.dumps(list_values)})



@admin_only
def createforms(request):
    if request.method == 'POST':
        namemission = request.POST.get('missionname')
        codeform = request.POST.get('htmlcode')
        os.chdir('enqueteur/templates/EnqueteurPage')
        file = codecs.open(str(namemission)+'.html', "w", encoding="utf-8")
        file.write(codeform)
        file.close()
        savepage = CreateForms.objects.create(nameform=namemission, coreform=codeform)
        savepage.save()
        return HttpResponse('your template was created')
    return render(request, 'EnqueteurPage/createforms.html')

@csrf_exempt
@admin_only
def buildpage(request, mission):
    path = 'EnqueteurPage/'+str(mission)+'.html'
    listname = []
    if len(mission) > 1:
        lowermission = mission.lower()
        print(lowermission)
        getpage = CreateForms.objects.filter(nameform=lowermission).values()
        if len(getpage) > 0:
            for page in getpage:
                soup = BeautifulSoup(page.get('coreform'))
                s = soup.find_all(['input', 'select'])
                i = 0
                while i < len(s):
                    mylist = s[i].get('name')
                    if mylist != None:
                        listname.append(mylist)
                    i += 1
                # we got lit of names fields end
                for i in range(len(listname)):
                    data[listname[i]] = request.POST.get(listname[i])
                    mlist.append(request.GET.get(i))
                # New code here
                filtered = {k: v for k, v in data.items() if v is not None}
                data.clear()
                data.update(filtered)
                user = str(request.user)
                if len(data) != 0:
                    savedataform = SurveyData.objects.create(user=user,
                                                             nameform=lowermission,
                                                             date=datetime.datetime.now(),
                                                             data=json.dumps(data))
                    savedataform.save()
                    data.clear()
                    return redirect('createforms')
                # end of new code
                return HttpResponse(page.get('coreform'))
            else:
                return redirect('createforms')
        else:
            redirect('createforms')
    return render(request, path)
