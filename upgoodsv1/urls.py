"""upgoodsv1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from enqueteur import views
from django.conf.urls.static import static
from upgoodsv1 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('service/', views.service, name='service'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('auth_re_password/', views.auth_re_password, name='auth_re_password'),
    path('actualite/', views.actualite, name='actualite'),
    path('article/', views.actualite_detail, name='article_detail'),
    path('guide/', views.faq, name='guide'),
    path('contact/', views.contact, name='contact'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),


                  #Enqueteur
    path('indexEnqueteur/', views.indexEnqueteur, name='indexEnqueteur'),
    path('trouvermission/', views.Trouvermission, name='trouvermission'),
    path('mission_detail/', views.mission_detail, name='mission_detail'),
    path('apply_for_mission/', views.apply_for_mission, name='apply_for_mission'),
    path('mission/', views.mission, name='mission'),
    path('account_messages/', views.account_messages, name='account_messages'),
    path('account_payments/', views.account_payments, name='account_payments'),
    path('account_profile/', views.account_profile, name='account_profile'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('account_works/', views.account_works, name='account_works'),
    path('contact_enqueteur/', views.contact_enqueteur, name='contact_enqueteur'),
    path('createforms/', views.createforms, name='createforms'),
    path('createforms/<str:mission>', views.buildpage, name='createforms'),
    path('showdata/', views.showdata, name='showdata'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_changed/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_completed'),
                  #Administrateur
    path('indexAdmin/', views.indexAdmin, name='IndexAdmin'),
    path('IndexAdmin2/', views.IndexAdmin2, name='IndexAdmin2'),
    path('tableau/', views.tableau, name='tableau'),
    path('mailbox_read/', views.mailbox_read, name='mailbox_read'),
    path('mailbox/', views.mailbox, name='mailbox'),
    path('mailbox_compose/', views.mailbox_compose, name='mailbox_compose'),
    path('users_status/', views.users_status, name='users_status'),
    path('sent/', views.sent, name='sent'),
    path('servey/', views.servey, name='servey'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

