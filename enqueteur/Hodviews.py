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

data = {}
indice = 0
mlist = []
filtredNone = []


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
                    data[listname[i]] = request.POST.get(listname[i])
                    mlist.append(request.POST.get(i))
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


#Administrateur Views

def indexAdmin(request):
    return render(request, "Administrateur/index.html")


def IndexAdmin2(request):
    return render(request, "Administrateur/indexNew.html")

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

def users_status(request):
    return render(request, "Administrateur/projects.html")


def sent(request):
    return render(request, "Administrateur/mailbox/mail-sent.html")


def manage_forms(request):
    servey=CreateForms.objects.all()
    return render(request,"administrateur/gestion_forms.html",{"servey":servey})


def view_form(request,servey_id):
    servey=SurveyData.objects.get(id=servey_id)

    return render(request,"administrateur/edit_post.html",{"servey": servey})

def delete_form(request,servey_id):
    servey=CreateForms.objects.get(id=servey_id)
    servey.delete()
    return redirect("manage_forms")



def add_post(request):
    return render(request, "Administrateur/add_post.html")


def add_post_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:

        title = request.POST.get("title")
        content = request.POST.get("content")
        keywords = request.POST.get("keywords")

        try:

            actualite=Actualite(title=title, content=content,keywords=keywords)
            actualite.save()
            messages.success(request,"Successfully Added Post")
            return HttpResponseRedirect(reverse("add_post"))
        except:
            messages.error(request,"Failed To Add Post")
            return HttpResponseRedirect(reverse("add_post"))


def manage_post(request):
    post=Actualite.objects.all()
    return render(request,"administrateur/manage_post.html",{"post":post})


def edit_post(request,post_id):
    post = Actualite.objects.get(id=post_id)
    return render(request,"administrateur/edit_post.html",{"post": post})


def delete_post(request,post_id):
    post = Actualite.objects.get(id=post_id)
    post.delete()
    return redirect("manage_post")


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

def servey(request):
    return render(request, "Administrateur/servey.html")

def mailbox_compose(request):
    return render(request, "Administrateur/mailbox/compose.html")

def mailbox(request):
    return render(request, "Administrateur/mailbox/mailbox.html")

def mailbox_read(request):
    return render(request, "Administrateur/mailbox/read-mail.html")

