from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
#from verify_email.email_handler import send_verification_email

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
import smtplib
from upgoodsv1 import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from django.views import View
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site

data = {}
indice = 0
mlist = []
filtredNone = []
averge_list = []
approuve_data_staff = {}
approuve_data_mail = {}
email_data = {}

jdata = {}
list_image_name = []


def sendemail_fattah(to_email, bd, sub):
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'gwbglboljgephemw'

    sent_from = gmail_user
    to = [to_email]
    subject = sub
    body = bd
    message = EmailMultiAlternatives(subject=subject, body=bd, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email_conf.html", {'key': email_data})
    message.attach_alternative(html_template, "text/html")
    try:
        message.send()

        print('Email sent!')
    except:
        print('Something went wrong...')


@csrf_exempt
def handicap(request):
    return render(request, "Homepage/formhandicap.html")


@csrf_exempt
@login_required
def handicap_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("handicap"))
    else:
        staff_obj = Enqueteur.objects.get(user=request.user)

        print(staff_obj)
        name = request.POST.get("field1")
        adresse = request.POST.get("adresse")
        code = request.POST.get("code")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        atteint_dun_handicap = request.POST.get("atteint_dun_handicap")
        membre_famille_atteint_dun_handicap = request.POST.get("membre_famille_atteint_dun_handicap")
        type_handicap = request.POST.get("type_handicap")
        evolution_handicap = request.POST.get("evolution_handicap")
        etes_vous_seul = request.POST.get("etes_vous_seul")
        temps_en_handicap = request.POST.get("temps_en_handicap")

    try:

        leave_report = Handicap(enqueteur_id=staff_obj,
                                data={'nom': name, 'adresse': adresse, 'code': code, 'ville': ville, 'pays': pays,
                                      'atteint_dun_handicap': atteint_dun_handicap,
                                      'membre_famille_atteint_dun_handicap': membre_famille_atteint_dun_handicap,
                                      'type_handicap': type_handicap, 'evolution_handicap': evolution_handicap,
                                      'etes_vous_seul': etes_vous_seul, 'temps_en_handicap': temps_en_handicap})
        leave_report.save()
        return HttpResponseRedirect(reverse("indexEnqueteur"))
    except:
        messages.error(request, "Failed To Apply for Leave")
        return HttpResponseRedirect(reverse("indexEnqueteur"))


def sendemailmsg(emailuser):
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'upgoodstest1234'

    sent_from = gmail_user
    to = [emailuser]
    subject = 'Vous avez un nouveau message'
    notif_message = 'vous avez recu un nouveau message'
    message = EmailMultiAlternatives(subject=subject, body=notif_message, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email_msg.html", {'key': approuve_data_mail})
    message.attach_alternative(html_template, "text/html")
    try:
        message.send()

        print('Email sent!')
    except:
        print('Something went wrong...')


# Views de l'Enqueteur


def testm(request):
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'upgoodstest1234'
    sent_from = gmail_user
    to = ['zahhaoui@gmail.com']
    subject = 'Bienvenue sur la plateforme UPGOODS'
    notif_message = 'Un nouveau enqueteur vient de s inscrire'
    message = EmailMultiAlternatives(subject=subject, body=notif_message, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email_confirmation.html")
    message.attach_alternative(html_template, "text/html")


def sendemail_mission():
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'upgoodstest1234'
    sent_from = gmail_user
    to = [approuve_data_staff.get('enqueteur_email')]
    pdfname = approuve_data_staff.get('mission_name')
    subject = 'GOOD NEWS!!'
    notif_message = 'Vous êtes selectionné pour une mission'
    message = EmailMultiAlternatives(subject=subject, body=notif_message, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email_mission.html", {'key': approuve_data_staff})
    message.attach_alternative(html_template, "text/html")
    attachment = open('media/media/mission_logo/Visite-Test.pdf', 'rb')
    message.attach('Visite-Test.pdf', attachment.read(), 'text/pdf')
    try:
        message.send()

        print('Email sent!')
    except:
        print('Something went wrong...')


def sendemail_confirmation(self):
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'upgoodstest1234'
    sent_from = gmail_user
    to = ['zahhaoui@gmail.com ']
    subject = 'Bienvenue sur la plateforme UPGOODS'
    notif_message = 'Un nouveau enqueteur vient de s inscrire'
    message = EmailMultiAlternatives(subject=subject, body=notif_message, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email_confirmation.html")
    message.attach_alternative(html_template, "text/html")

    try:
        message.send()

        print('Email sent!')
    except:
        print('Something went wrong...')


def sendemail(emailuser, username, created_at):
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'upgoodstest1234'

    sent_from = gmail_user
    to = ['client-mystere@amsinternational.fr']
    subject = 'Un nouveau enqueteur vient de s inscrire'
    notif_message = 'Un nouveau enqueteur vient de s inscrire'
    message = EmailMultiAlternatives(subject=subject, body=notif_message, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email.html",
                                     {"emailuser": emailuser, "username": username, "created_at": created_at})
    message.attach_alternative(html_template, "text/html")
    try:
        message.send()

        print('Email sent!')
    except:
        print('Something went wrong...')


# Views de l'Enqueteur

def text(request):
    return render(request, "new/index-customer.html")


def testt(email):
    gmail_user = 'upgoodstest@gmail.com'
    gmail_password = 'upgoodstest1234'
    sent_from = gmail_user
    to = ['email']
    subject = 'Bienvenue sur la plateforme UPGOODS'
    notif_message = 'Un nouveau enqueteur vient de s inscrire'
    message = EmailMultiAlternatives(subject=subject, body=notif_message, from_email=sent_from, to=to)
    html_template = render_to_string("Homepage/email_confirmation.html")
    message.attach_alternative(html_template, "text/html")

    try:
        message.send()

        print('Email sent!')
    except:
        print('Something went wrong...')


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
    return render(request, "EnqueteurPage/page-jobs-sidebar.html", context)


@login_required
def mission(request):
    servey = SurveyData.objects.filter(user=request.user.id).first()
    candidature = Candidature.objects.all().filter(enqueteur_id__user=request.user)
    context = {
        'servey': servey,
        'candidature': candidature
    }
    return render(request, "EnqueteurPage/page-blog-grid.html", context)


@login_required
def mission_detail_apply(request, post_id):
    post = Mission.objects.get(id=post_id)

    return render(request, "EnqueteurPage/page-job-detail_apply.html", {'post': post})


def testxxx(request):
    return render(request, "EnqueteurPage/page-job-detail_apply.html")


def testte(request):
    return render(request, "questionnairetest.html")


@login_required
def mission_detail(request, post_id):
    ls = []
    post = Mission.objects.get(id=post_id)
    candidature = Candidature.objects.filter(enqueteur_id__user=request.user).values()
    if len(candidature) == 0:
        ls.clear()
        ls.append({'candidature_status' == 3})
    else:
        for i in candidature:
            if int(i['mission_id_id']) == int(post_id):
                ls.clear()
                ls.append(i)
            if len(ls) == 0:
                ls.clear()
                ls.append({'candidature_status' == 3})
    return render(request, "EnqueteurPage/page-job-detail.html", {'post': post, 'candidature': ls})


# candidature

@login_required
def staff_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("apply_for_mission"))
    else:
        staff_obj = Enqueteur.objects.get(user=request.user)
        mission_id = request.POST.get("mission_id")

        motivation = request.POST.get("motivation")
        date = request.POST.get("date")

        try:
            mission_obj = Mission.objects.get(id=mission_id)
            leave_report = Candidature(enqueteur_id=staff_obj, mission_id=mission_obj, motivation=motivation,
                                       candidature_status=0, date_visite=date)

            leave_report.save()
            messages.success(request,
                             "Parfait, votre candidature est transmise a notre service relation pour la verification")
            return HttpResponseRedirect(reverse("mission_detail_apply", kwargs={"post_id": mission_id}))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("mission_detail_apply", kwargs={"post_id": mission_id}))


# validation des candidatures


@login_required
def apply_for_mission(request, mission_id):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    mission = Mission.objects.get(id=mission_id)
    return render(request, "EnqueteurPage/page-job-apply.html", {"enqueteur": enqueteur, 'mission': mission})


@login_required
def delete_candidature(request, candidature_id):
    servey = Candidature.objects.get(id=candidature_id)
    servey.delete()
    return redirect('mission')


@admin_only
def staff_leave_view(request):
    leaves = Candidature.objects.get_queryset().order_by('-created_at')
    message_paginator = Paginator(leaves, 5)
    page_num = request.GET.get('page')
    page = message_paginator.get_page(page_num)
    context = {
        'count': message_paginator.count,
        'page': page,
        'leaves': leaves,
    }
    return render(request, "Administrateur/staff_leave_view.html", context)


@admin_only
def staff_approve_leave(request, leave_id):
    leave = Candidature.objects.get(id=leave_id)
    leave.candidature_status = 1
    leave.save()
    leave_saved = Candidature.objects.filter(id=leave_id).values()
    leave_data = leave_saved[0]
    enqueteur = Enqueteur.objects.filter(id=leave_data['enqueteur_id_id']).values()
    mission = Mission.objects.filter(id=leave_data['mission_id_id']).values()
    organisme = Organisme.objects.filter(id=mission[0].get('organisme_id')).values()
    approuve_data_staff['organisme_name'] = organisme[0].get('nom')
    approuve_data_staff['enqueteur_name'] = enqueteur[0].get('nom')
    approuve_data_staff['enqueteur_email'] = enqueteur[0].get('email')
    approuve_data_staff['mission_name'] = mission[0].get('nom')
    approuve_data_staff['mission_ville'] = mission[0].get('ville')
    approuve_data_staff['mission_pays'] = mission[0].get('pays')
    approuve_data_staff['mission_debut'] = mission[0].get('date_debut')
    approuve_data_staff['mission_fin'] = mission[0].get('date_fin')
    sendemail_mission()
    approuve_data_staff.clear()
    return HttpResponseRedirect(reverse("staff_leave_view"))


@admin_only
def staff_disapprove_leave(request, leave_id):
    leave = Candidature.objects.get(id=leave_id)
    leave.candidature_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


@login_required
def account_messages(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user.id)
    message = Contact_admin.objects.get_queryset().filter(enqueteur_id=enqueteur.id).order_by('-created_at')
    message_paginator = Paginator(message, 5)
    page_num = request.GET.get('page')
    page = message_paginator.get_page(page_num)
    context = {
        'count': message_paginator.count,
        'page': page,
        'message': message,
        'enqueteur': enqueteur
    }
    return render(request, "EnqueteurPage/account-messages.html", context)


@login_required
def account_payments(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user.id)
    remu_enqueteur = Remuneration_table.objects.filter(enqueteur_id__user=user).values()
    print(mission)
    for c in remu_enqueteur:
        if c['status'] == 0:
            c['status'] = 'En cours'
        if c['status'] == 1:
            c['status'] = 'Payé'
        if c['status'] == 2:
            c['status'] = 'Refusé'
    return render(request, "EnqueteurPage/account-payments.html",
                  {"remu_enqueteur": remu_enqueteur, "enqueteur": enqueteur})


@admin_only
def builder(request):
    return render(request, "index.html")


@login_required
def account_profile(request):
    try:
        user = request.user
        enqueteur = Enqueteur.objects.get(user=user)
        post = Actualite.objects.all()
        message_paginator = Paginator(post, 4)
        page_num = request.GET.get('page')
        page = message_paginator.get_page(page_num)
        context = {
            'count': message_paginator.count,
            'page': page,
            'post': post,
            'enqueteur': enqueteur,
        }
    except Enqueteur.DoesNotExist:
        return redirect('questionnaire')
    return render(request, "EnqueteurPage/account-profile.html", context)


@login_required
@csrf_exempt
def updateprofil(request):
    getprofildata = Enqueteur.objects.filter(user=request.user).values()
    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        if len(telephone) and len(email) and len(adresse) != 0:
            Enqueteur.objects.filter(user=request.user).update(telephone=telephone,
                                                               email=email,
                                                               adresse=adresse)
            print('data saved')
        else:
            print('you have to fill all fields')
    else:
        print('data wasnt saved')
    return render(request, 'EnqueteurPage/account-setting.html', {'data': getprofildata[0]})


@login_required
def account_works(request):
    user = request.user
    enqueteur = Enqueteur.objects.get(user=user)
    candidature = Candidature.objects.all().filter(enqueteur_id__user=request.user)
    return render(request, "EnqueteurPage/account-works.html", {"enqueteur": enqueteur, "candidature": candidature})


@login_required
def contact_enqueteur(request):
    return render(request, "EnqueteurPage/page-contact-one.html")


# Views D'acceuil

def index(request):
    return render(request, "Homepage/index-services.html")




def panel(request):
    return render(request, "Homepage/index-customer.html")


def dem(request):
    return render(request, "new/demo.html")


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
        'categorie': categorie,
    }
    return render(request, "Homepage/page-blog-list.html", context)


def actualite_detail(request, post_id):
    post = Actualite.objects.get(id=post_id)

    return render(request, "Homepage/page-blog-detail-two.html", {"post": post})


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
        comments = request.POST.get('comments')
        try:
            contact = Contact_enqueteur.objects.create(enqueteur_id=enqueteur, comments=comments)
            contact.save()
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return HttpResponseRedirect('/account_messages')
        except:
            return HttpResponseRedirect('/account_messages')


# Contact Message
@csrf_exempt
def contact_sent(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        comments = request.POST.get('comments')
        try:
            contact = Contact.objects.create(name=name, email=email, subject="From contact form", comments=comments)
            contact.save()
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return HttpResponseRedirect('/contact')
        except:
            return HttpResponseRedirect('/contact')


# Register
@csrf_exempt
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = createUser()
        if request.method == 'POST':
            form = createUser(request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.get(username=form.cleaned_data.get('username'))
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_data['user'] = user
                email_data['domain'] = current_site.domain
                email_data['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
                email_data['token'] = account_activation_token.make_token(user)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                link = reverse('activate', kwargs={
                    'uidb64': email_body['uid'], 'token': email_body['token']})

                activate_url = 'http://' + current_site.domain + link
                email_subject = 'Activate your account'

                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                sendemail_fattah(email, activate_url, email_subject)
                email_data.clear()
                # created_at = datetime.datetime.now()
                # sendemail(username, email,created_at)
                messages.success(request, 'Votre nouveau compte a été créé avec succès {} . Veuillez vérifier votre courriel pour l activation de votre compte'.format(username))
                return redirect('login')
        return render(request, 'Homepage/auth-signup-three.html', {'form': form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'Utilisateur déjà activé ')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Votre compte a été activé avec succès')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


# Validation des comptes :

def questionnaire(request):
    url = ''
    if request.method == 'POST':
        nom = request.POST.get('nom')
        birth_day = request.POST.get('birth_day')
        genre = request.POST.get('genre')
        telephone = request.POST.get('full_number')
        adresse = request.POST.get('adresse')
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')
        zipcode = request.POST.get('zipcode')
        ordinateur = request.POST.get('ordinateur')
        vehicule = request.POST.get('vehicule')
        userexp = request.POST.get('userexp')
        expmois = request.POST.get('expmois')
        societe = request.POST.get('societe')
        lunettes = request.POST.get('lunettes')
        logement = request.POST.get('logement')
        habitation = request.POST.get('habitation')
        langues = request.POST.get('debug')
        meilleur = request.POST.get('meilleur')
        pire = request.POST.get('pire')
        restaurant = request.POST.get('restaurant')
        situation = request.POST.get('situation')
        joindre = request.POST.get('joindre')
        enfants = request.POST.get('enfants')
        try:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            url = profile_pic_url
        except MultiValueDictKeyError:
            url = ''

        created_at = datetime.datetime.now()
        email = request.user.email
        adresse_c = adresse + " " + zipcode + " " + pays + " " + ville
        status = True
        user = request.user
        enqueteur = Enqueteur.objects.create(user=user,
                                             nom=nom,
                                             profile_pic=url,
                                             email=email,
                                             created_at=created_at,
                                             adresse=adresse_c,
                                             # latitude=latitude,
                                             ordinateur=ordinateur,
                                             vehicule=vehicule,
                                             # longitude=longitude,
                                             birth_day=birth_day,
                                             telephone=telephone,
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
        enqueteur.save()
        return redirect('indexEnqueteur')

    return render(request, 'questionnaire.html')


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('indexEnqueteur')
    else:
        if request.method == 'POST':
            email = request.POST.get('username')
            password = request.POST.get('password')
            try:
                username = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.info(request, 'your password or username not correct')
                return render(request, 'Homepage/auth-login.html')
            user = authenticate(request, username=username.username, password=password)
            if user.is_active == False:
                messages.info(request, 'Verifier votre boite mail avant de se connecter ')

            if user is not None:
                dj_login(request, user)
                try:
                    if request.user.is_superuser:
                        return redirect('IndexAdmin')
                    else:
                        currentuser = Enqueteur.objects.get(user=request.user)
                        if len(currentuser.nom) > 0:
                            return redirect('indexEnqueteur')
                except Enqueteur.DoesNotExist:
                    return redirect('questionnaire')
            else:
                messages.info(request, 'votre mot de passe ou adresse email est incorrect')
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


# Administrateur Views
@admin_only
def indexAdmin(request):
    consultant_count1 = Enqueteur.objects.all().count()
    mission_count = Mission.objects.all().count()

    context = {
        'consultant_count1': consultant_count1,
        'mission_count': mission_count
    }
    return render(request, "Administrateur/index.html", context)


@admin_only
def test(request):
    return render(request, "Administrateur/forms/general.html")


def testquestionnaire(request):
    return render(request, "questionnairetest.html")


@admin_only
def IndexAdmin2(request):
    return render(request, "Administrateur/indexNew.html")


def testx(request):
    return render(request, "Homepage/promotional.html")


def testxx(request):
    return render(request, "Homepage/general.html")


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
    return render(request, "Administrateur/tables/data.html",
                  {'surveydata': surveydata, 'data': json_list, 'head': headelement.keys()})


# gestion des enqueteurs

@admin_only
def users_status(request):
    users = Enqueteur.objects.all()
    userss = User.objects.all()
    return render(request, "Administrateur/projects.html", {'users': users, 'userss': userss})


@admin_only
def profile(request, enqueteur_id):
    enqueteur = Enqueteur.objects.get(id=enqueteur_id)
    return render(request, "Administrateur/profile.html", {'enqueteur': enqueteur})


# Mappage des enqueteurs

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


# Affichage des resultats des missions

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


@csrf_exempt
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


# gestion des formulaires

@admin_only
def manage_forms(request):
    servey = CreateForms.objects.all()
    return render(request, "Administrateur/gestion_forms.html", {"servey": servey})


@admin_only
def view_form(request, servey_id):
    servey = SurveyData.objects.get(id=servey_id)

    return render(request, "Administrateur/edit_post.html", {"servey": servey})


@admin_only
def delete_form(request, servey_id):
    servey = CreateForms.objects.get(id=servey_id)
    servey.delete()
    return redirect("manage_forms")


# gestion des missions + organismes

@admin_only
def manage_mission(request):
    organisme = Organisme.objects.all()
    mission = Mission.objects.all()

    servey = CreateForms.objects.all()

    return render(request, "Administrateur/manage_mission.html",
                  {'organisme': organisme, "servey": servey, 'mission': mission})


@admin_only
def add_organisme_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:

        nom = request.POST.get("nom")
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        profile_pic_url = fs.url(filename)
        try:

            organisme = Organisme(nom=nom, photo=photo)
            organisme.profile_pic = profile_pic_url
            organisme.save()
            messages.success(request, "Successfully Added organisme")
            return HttpResponseRedirect(reverse("manage_mission"))
        except:
            messages.error(request, "Failed To Add organisme")
            return HttpResponseRedirect(reverse("manage_mission"))


@admin_only
def add_mission_save(request):
    if request.method != "POST":
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

            mission = Mission(ref=ref, nom=nom, thematique=thematique, remuneration=remuneration,
                              description=description, date_debut=date_debut, date_fin=date_fin, ville=ville, pays=pays)
            quizz_obj = CreateForms.objects.get(id=quizz_id)
            mission.questionnaire = quizz_obj
            organisme_obj = Organisme.objects.get(id=organisme_id)
            mission.organisme = organisme_obj

            mission.save()
            messages.success(request, "Successfully Added mission")
            return HttpResponseRedirect(reverse("manage_mission"))
        except:
            messages.error(request, "Failed To Add mission")
            return HttpResponseRedirect(reverse("manage_mission"))


@admin_only
def edit_mission(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    organisme = Organisme.objects.all()
    servey = CreateForms.objects.all()
    context = {
        'organisme': organisme,
        "servey": servey,
        "mission": mission
    }
    return render(request, "Administrateur/edit_mission.html", context)


@admin_only
def edit_mission_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        mission_id = request.POST.get("mission_id")
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
        # try:

        mission = Mission.objects.get(id=mission_id)
        mission = Mission(ref=ref, nom=nom, thematique=thematique, remuneration=remuneration, description=description,
                          date_debut=date_debut, ville=ville, pays=pays)
        mission.date_fin = date_fin
        quizz_obj = CreateForms.objects.get(id=quizz_id)
        mission.questionnaire = quizz_obj
        organisme_obj = Organisme.objects.get(id=organisme_id)
        mission.organisme = organisme_obj

        mission.save()
        # messages.success(request,"Successfully Edited mission")
        #    return HttpResponseRedirect(reverse("edit_mission",kwargs={"mission_id":mission_id}))
        # except:
        #   messages.error(request,"Failed To Edit mission")
        #  return HttpResponseRedirect(reverse("edit_mission",kwargs={"mission_id":mission_id}))


@admin_only
def delete_mission(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    mission.delete()
    return redirect("manage_mission")


# validation de la visite


@admin_only
def validation_visite(request):
    servey = SurveyData.objects.all()

    return render(request, "Administrateur/validation_visite.html", {"servey": servey})


@admin_only
def staff_approve_profile(request, enqueteur_id):
    user = Enqueteur.objects.get(id=enqueteur_id)
    user.verification = 1
    user.save()

    return HttpResponseRedirect(reverse("users_status"))


@admin_only
def staff_disapprove_profile(request, enqueteur_id):
    user = Enqueteur.objects.get(id=enqueteur_id)
    user.verification = 2
    user.save()
    return HttpResponseRedirect(reverse("users_status"))


@admin_only
def staff_approve_visite(request, survey_id):
    leave = CreateForms.objects.get(id=survey_id)
    leave.visite_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("validation_visite"))


@admin_only
def staff_disapprove_visite(request, survey_id):
    leave = CreateForms.objects.get(id=survey_id)
    leave.visite_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("validation_visite"))


# Gestion d'actualité

@admin_only
def add_post_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:

        title = request.POST.get("title")
        content = request.POST.get("content")
        keywords = request.POST.get("keywords")
        photo = request.POST.get("photo")

        try:

            actualite = Actualite(title=title, content=content, keywords=keywords, photo=photo)
            actualite.save()
            messages.success(request, "Successfully Added Post")
            return HttpResponseRedirect(reverse("manage_post"))
        except:
            messages.error(request, "Failed To Add Post")
            return HttpResponseRedirect(reverse("manage_post"))


@admin_only
def manage_post(request):
    post = Actualite.objects.all()
    return render(request, "Administrateur/manage_post.html", {"post": post})


@admin_only
def edit_post(request, post_id):
    post = Actualite.objects.get(id=post_id)
    return render(request, "Administrateur/edit_post.html", {"post": post})


@admin_only
def delete_post(request, post_id):
    post = Actualite.objects.get(id=post_id)
    post.delete()
    return redirect("manage_post")


@admin_only
def edit_post_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        post_id = request.POST.get("post_id")
        title = request.POST.get("title")
        content = request.POST.get("content")
        keywords = request.POST.get("keywords")

        try:
            post = Actualite.objects.get(id=post_id)
            post.title = title
            post.content = content
            post.keywords = keywords
            post.save()
            messages.success(request, "Successfully Edited post")
            return HttpResponseRedirect(reverse("edit_post", kwargs={"post_id": post_id}))
        except:
            messages.error(request, "Failed to Edit post")
            return HttpResponseRedirect(reverse("edit_post", kwargs={"post_id": post_id}))


# Serveyjs demo

@admin_only
def servey(request):
    return render(request, "Administrateur/servey.html")


# gestion des messages INBOX

@admin_only
def sent(request):
    return render(request, "Administrateur/mailbox/mail-sent.html")


@admin_only
def mailbox_compose(request):
    return render(request, "Administrateur/mailbox/compose.html")


@admin_only
def mailbox_compose_envoie(request, enqueteur_id):
    user = Enqueteur.objects.get(id=enqueteur_id)
    return render(request, "Administrateur/mailbox/compose.html", {'user': user})


@admin_only
def mailbox_compose_envoie_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:

        enqueteur_id = request.POST.get("enqueteur_id")
        reply = request.POST.get("reply")

        try:
            post = Contact_admin(reply=reply)
            quizz_obj = Enqueteur.objects.get(id=enqueteur_id)

            post.enqueteur_id = quizz_obj
            enqueteur = Enqueteur.objects.filter(id=enqueteur_id).values()
            emailuser = approuve_data_mail['email'] = enqueteur[0].get('email')
            username = approuve_data_mail['nom'] = enqueteur[0].get('nom')
            approuve_data_mail['reply'] = reply
            created_at = approuve_data_mail['created_at'] = datetime.datetime.now()
            post.save()
            sendemailmsg(emailuser)
            approuve_data_mail.clear()

            messages.success(request, "Le message est transmis avec succés ")
            return HttpResponseRedirect(reverse("profile", kwargs={"enqueteur_id": enqueteur_id}))
        except:
            messages.error(request, "Error 404")
            return render(request, "Administrateur/profile.html", {'enqueteur_id': enqueteur_id})


@admin_only
def mailbox(request):
    contact = Contact.objects.all()
    contact_enqueteur = Contact_enqueteur.objects.all()
    message_count = Contact.objects.all().count()
    message_countt = Contact_enqueteur.objects.all().count()
    me = message_count + message_countt

    context = {'contact': contact,
               'contact_enqueteur': contact_enqueteur,
               'message_count': message_count,
               'me': me
               }
    return render(request, "Administrateur/mailbox/mailbox.html", context)


@admin_only
def mailbox_read_enqueteur(request, message_id):
    message = Contact_enqueteur.objects.get(id=message_id)
    return render(request, "Administrateur/mailbox/read-mail_enqueteur.html", {'message': message})


@admin_only
def mailbox_read_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, "Administrateur/mailbox/read-mail.html", {'contact': contact})


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
                return HttpResponse('Erreur 404 contactez l equipe dev ')

    except IndexError:
        return HttpResponse('this url or mission doesnt exist...')
    return render(request, 'Administrateur/tables/averge.html', {'key': list_keys,
                                                                 'value': list_values,
                                                                 'jsonkey': json.dumps(list_keys),
                                                                 'jsonvalue': json.dumps(list_values)})


def validationx(request):
    return render(request, 'Administrateur/valid.html')


def createforms(request):
    if request.method == 'POST':
        namemission = request.POST.get('missionname')
        codeform = request.POST.get('htmlcode')
        os.chdir('./enqueteur/templates/EnqueteurPage')
        file = codecs.open(str(namemission) + '.html', "w", encoding="utf-8")
        file.write(codeform)
        file.close()
        savepage = CreateForms.objects.create(nameform=namemission, coreform=codeform)
        savepage.save()
        return HttpResponse('your template was created')
    return render(request, 'EnqueteurPage/createforms.html')


@csrf_exempt
def buildpage(request, mission):
    path = 'EnqueteurPage/' + str(mission) + '.html'
    listname = []
    if len(mission) > 1:
        lowermission = mission.lower()
        getpage = CreateForms.objects.filter(nameform=lowermission).values()
        if len(getpage) > 0:
            for page in getpage:
                soup = BeautifulSoup(page.get('coreform'), "html.parser")
                s = soup.find_all(['input', 'select', 'textarea'])
            print(s)
            i = 0
            while i < len(s):
                mylist = s[i].get('name')
                if mylist != None:
                    listname.append(mylist)
                i += 1
            for i in s:
                if i.get("type") == "file":
                    list_image_name.append(i.get("name"))
            # print(list_image_name)
            # we got list of names fields end
            for i in range(len(listname)):
                data[listname[i]] = request.POST.get(listname[i])
                # mlist.append(request.GET.get(i))
            if len(request.FILES) != 0:
                ls_name_image = list(dict.fromkeys(list_image_name))
                for index in range(len(ls_name_image)):
                    pic = request.FILES[list_image_name[index]]
                    fs = FileSystemStorage()
                    filename = fs.save(pic.name, pic)
                    pic_url = fs.url(filename)
                    data['pic' + str(index)] = pic_url

                # New code here
            # filtered = {k: v for k, v in data.items() if v is not None}
            # data.clear()
            # data.update(filtered)

            user = str(request.user)
            if len(data) != 0 and request.method == "POST":
                savedataform = SurveyData.objects.create(user=user,
                                                         nameform=lowermission,
                                                         date=datetime.datetime.now(),
                                                         data=json.dumps(data))
                savedataform.save()
                data.clear()
                return render(request, 'Administrateur/valid.html')

            # end of new code

    return render(request, path)


@admin_only
@csrf_exempt
def data_each_mission(request):
    head = ['id', 'date', 'nameform', 'user', 'visite_status', 'voir', 'valider', 'refuser', 'payer', 'refuser_pay']
    listmission = []
    json_list = []
    retrieve_data = SurveyData.objects.all().values()
    for i in range(len(retrieve_data)):
        listmission.append(retrieve_data[i]['nameform'])
    mylist = list(dict.fromkeys(listmission))
    if request.method == 'POST':
        mission = request.POST.get('mission')
        retrivedata = SurveyData.objects.filter(nameform=mission).values()
        if retrivedata:
            for i in retrivedata:
                dict_data = {}
                dict_data['id'] = i.get('id')
                dict_data['date'] = i.get('date')
                dict_data['nameform'] = i.get('nameform')
                dict_data['user'] = i.get('user')
                dict_data['visite_status'] = i.get('visite_status')
                json_list.append(dict_data)
            for c in json_list:
                if c.get('visite_status') == 0:
                    c['visite_status'] = 'pending'
                if c.get('visite_status') == 1:
                    c['visite_status'] = 'accepted'
                if c.get('visite_status') == 2:
                    c['visite_status'] = 'refused'
        else:
            print('no data gotten')
    return render(request, 'Administrateur/data_each_mission.html', {'listmission': mylist, 'head': head,
                                                                     'brinv_list': json_list})


@csrf_exempt
@admin_only
def approuve_survey(request, id):
    survey = SurveyData.objects.get(id=id)
    survey.visite_status = 1
    survey.save()

    msurvey = SurveyData.objects.filter(id=id).values()
    data = msurvey[0]
    id = data['id']
    mission = survey.nameform
    user = data['user']
    date = data['date']
    mission_remun = Mission.objects.filter(questionnaire__nameform=mission).values()
    remuneration = mission_remun[0].get('remuneration')
    enqueteur = Enqueteur.objects.get(user__username=user)
    try:
        remun = Remuneration_table.objects.get(id_survey=id)
        remun.status = 0
        remun.save()
    except Remuneration_table.DoesNotExist:
        Remuneration_table.objects.create(id_survey=id,
                                          mission_id=mission,
                                          remuneration=remuneration,
                                          enqueteur_id=enqueteur,
                                          date_envoie=date,
                                          status=0
                                          )
    return render(request, 'Administrateur/approuve_survey.html')


@admin_only
def refuse_survey(request, id):
    survey = SurveyData.objects.get(id=id)
    survey.visite_status = 2
    survey.save()
    return render(request, 'Administrateur/refuse_survey.html')


@admin_only
def remun_send(request, id):
    remun = Remuneration_table.objects.get(id_survey=id)
    remun.status = 1
    remun.save()
    return render(request, 'Administrateur/remun_pay.html')


@admin_only
def refuse_remun(request, id):
    remun = Remuneration_table.objects.get(id_survey=id)
    remun.status = 2
    remun.save()
    return render(request, 'Administrateur/refuse_remun.html')
