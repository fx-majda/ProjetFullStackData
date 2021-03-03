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
from django.conf.urls import url
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
    path('actualite_detail//<str:post_id>', views.actualite_detail, name='actualite_detail'),
    path('guide/', views.faq, name='guide'),
    path('contact/', views.contact, name='contact'),
    path('contact_sent/', views.contact_sent, name='contact_sent'),
    path('profile/<str:enqueteur_id>', views.profile, name='profile'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

                  #Enqueteur
    path('indexEnqueteur/', views.indexEnqueteur, name='indexEnqueteur'),
    path('trouvermission/', views.Trouvermission, name='trouvermission'),
    path('mission_detail/<str:post_id>', views.mission_detail, name='mission_detail'),
    path('apply_for_mission/', views.apply_for_mission, name='apply_for_mission'),
    path('staff_apply_leave_save/', views.staff_apply_leave_save, name='staff_apply_leave_save'),
    path('mission/', views.mission, name='mission'),
    path('account_messages/', views.account_messages, name='account_messages'),
    path('account_payments/', views.account_payments, name='account_payments'),
    path('account_profile/', views.account_profile, name='account_profile'),
    path('account_settings/', views.updateprofil, name='account_settings'),
    path('account_works/', views.account_works, name='account_works'),
    path('contact_enqueteur/', views.contact_enqueteur, name='contact_enqueteur'),
    path('createforms/', views.createforms, name='createforms'),
    path('createforms/<str:mission>', views.buildpage, name='createforms'),
    path('showdata/', views.showdata, name='showdata'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='Homepage/auth-re-password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_changed/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_completed'),
                  #Administrateur
    path('indexAdmin/', views.indexAdmin, name='IndexAdmin'),
                  path('maps/', views.gpsmap, name='gpsmap'),
                  path('filterUserMission/<str:mission>/<str:user>', views.filterUserMission, name='filterUserMission'),


                  path('add_post/', views.add_post, name='add_post'),
    path('add_post_save/', views.add_post_save, name='add_post_save'),
    path('edit_post/<str:post_id>', views.edit_post, name="edit_post"),
    path('edit_post_save', views.edit_post_save, name="edit_post_save"),
                  path('staff_leave_view', views.staff_leave_view, name="staff_leave_view"),
                  path('staff_disapprove_leave/<str:leave_id>', views.staff_disapprove_leave,
                       name="staff_disapprove_leave"),
                  path('staff_approve_leave/<str:leave_id>', views.staff_approve_leave, name="staff_approve_leave"),

                  path('delete_post/<str:post_id>', views.delete_post, name="delete_post "),
                  path('delete_form/<str:servey_id>', views.delete_form, name="delete_form "),

                  path('manage_post', views.manage_post, name="manage_post"),
    path('manage_forms', views.manage_forms, name="manage_forms"),
    path('IndexAdmin2/', views.IndexAdmin2, name='IndexAdmin2'),
    path('tableau/', views.tableau, name='tableau'),
    path('mailbox_read/', views.mailbox_read, name='mailbox_read'),
    path('mailbox/', views.mailbox, name='mailbox'),
    path('mailbox_compose/', views.mailbox_compose, name='mailbox_compose'),
    path('users_status/', views.users_status, name='users_status'),
    path('sent/', views.sent, name='sent'),
    path('servey/', views.servey, name='servey'),
    path('createforms/', views.createforms, name='createforms'),
    path('createforms/<str:mission>', views.buildpage, name='createforms'),
    path('missiontest/', views.missiontest, name='missiontest'),

                  path('showdata/', views.showdata, name='showdata')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

