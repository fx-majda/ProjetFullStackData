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


def account_settings(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    getprofildata = Enqueteur.objects.filter(user=request.user).values()
    if getprofildata:
        profildatajson = json.dumps(getprofildata[0], sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        if request.method == 'POST':
            if request.POST.get('senddata'):
                data = request.POST.get('senddata')
                data_dict = json.loads(data)
                Enqueteur.objects.filter(user=request.user).update(telephone=data_dict['telephone'],
                                                                   email=data_dict['email'],
                                                                   adresse=data_dict['adresse'])
                print('data saved and updated.....')
        else:
            print('noooooo data gotten')
    else:
        print('not data existing')


    return render(request, "EnqueteurPage/account-setting.html",{"enqueteur":enqueteur,"data": profildatajson} )

def account_works(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    return render(request, "EnqueteurPage/account-works.html",{"enqueteur":enqueteur})

def contact_enqueteur(request):
    return render(request, "EnqueteurPage/page-contact-one.html")


#Views D'acceuil
def index(request):
    return render(request, "Homepage/index-services.html")

def service(request):
    return render(request, "Homepage/page-services.html")

def auth_re_password(request):
    return render(request, "Homepage/auth-re-password.html")

def actualite(request):
    return render(request, "Homepage/page-blog-list.html")

def actualite_detail(request):
    return render(request, "Homepage/page-blog-detail-two.html")

def faq(request):
    return render(request, "Homepage/helpcenter-faqs.html")

def contact(request):
    return render(request, "Homepage/page-contact-one.html")

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

@login_required(login_url='login')
@csrf_exempt
def updateprofil(request):
    getprofildata = Enqueteur.objects.filter(user=request.user).values()
    if getprofildata:
        profildatajson = json.dumps(getprofildata[0], sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        if request.method == 'POST':
            if request.POST.get('senddata'):
                data = request.POST.get('senddata')
                data_dict = json.loads(data)
                Enqueteur.objects.filter(user=request.user).update(telephone=data_dict['telephone'],
                                                                   email=data_dict['email'],
                                                                   adresse=data_dict['adresse'])
                print('data saved and updated.....')
        else:
            print('noooooo data gotten')
    else:
        print('not data existing')


    return render(request, 'updateprofil.html', {'data': profildatajson})



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


def createforms(request):
    if request.method == 'POST':
        namemission = request.POST.get('missionname')
        codeform = request.POST.get('htmlcode')
        savepage = CreateForms.objects.create(nameform=namemission, coreform=codeform)
        savepage.save()
        # getpage = CreateForms.objects.filter(nameform=namemission).values()
        # return HttpResponse(getpage)
        # return HttpResponse(getpage.codeform)
    return render(request, 'createforms.html')

@csrf_exempt
def buildpage(request, mission):
    listname = []
    if len(mission) > 1:
        lowermission = mission.lower()
        print(lowermission)
        getpage = CreateForms.objects.filter(nameform=lowermission).values()
        if len(getpage) > 0:
            for page in getpage:
                soup = BeautifulSoup("""{}""".format(page.get('coreform')))
                s = soup.find_all(['input', 'select'])
                i = 0
                while i < len(s):
                    mylist = s[i].get('name')
                    if mylist != None:
                        listname.append(mylist)
                    i += 1
                for i in range(len(listname)):
                    data[listname[i]] = request.GET.get(listname[i])
                    mlist.append(request.GET.get(i))
                print(listname)
                print(data)
                # New code here
                filtered = {k: v for k, v in data.items() if v is not None}
                data.clear()
                data.update(filtered)
                print(data)
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
                return HttpResponse("""{}""".format(page.get('coreform')))
        else:
            return redirect('createforms')
    else:
        redirect('createforms')

def showdata(request):
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
    return render(request, 'showdata.html', {'data': json_list, 'head': headelement.keys()})





def logoutuser(request):
    logout(request)
    return HttpResponseRedirect('/login/')


#Administrateur Views

def indexAdmin(request):
    return render(request, "Administrateur/index.html")


def IndexAdmin2(request):
    return render(request, "Administrateur/indexNew.html")

def tableau(request):
    return render(request, "Administrateur/tables/data.html")

def users_status(request):
    return render(request, "Administrateur/projects.html")


def sent(request):
    return render(request, "Administrateur/mailbox/mail-sent.html")


def servey(request):
    return render(request, "Administrateur/servey.html")

def mailbox_compose(request):
    return render(request, "Administrateur/mailbox/compose.html")

def mailbox(request):
    return render(request, "Administrateur/mailbox/mailbox.html")

def mailbox_read(request):
    return render(request, "Administrateur/mailbox/read-mail.html")