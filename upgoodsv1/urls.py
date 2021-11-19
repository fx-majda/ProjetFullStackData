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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from enqueteur import views
from django.conf.urls.static import static
from upgoodsv1 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(), name='activate'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
                  path('add_organisme_save/', views.add_organisme_save, name='add_organisme_save'),
                  path('add_mission_save/', views.add_mission_save, name='add_mission_save'),
                  path('edit_mission/<str:mission_id>', views.edit_mission, name="edit_mission"),
                  path('edit_mission_save', views.edit_mission_save, name="edit_mission_save"),
                  path('edit_mission/<str:mission_id>', views.edit_mission, name="edit_mission"),
                  path('delete_mission/<str:mission_id>', views.delete_mission, name="delete_mission"),
                  # poste
                  path('add_post_save/', views.add_post_save, name='add_post_save'),
                  path('edit_post/<str:post_id>', views.edit_post, name="edit_post"),
                  path('edit_post_save', views.edit_post_save, name="edit_post_save"),
                  path('staff_leave_view', views.staff_leave_view, name="staff_leave_view"),
                  path('staff_disapprove_leave/<str:leave_id>', views.staff_disapprove_leave,
                       name="staff_disapprove_leave"),
                  path('staff_approve_leave/<str:leave_id>', views.staff_approve_leave, name="staff_approve_leave"),
                  path('staff_disapprove_profile/<str:enqueteur_id>', views.staff_disapprove_profile,
                       name="staff_disapprove_profile"),
                  path('staff_approve_profile/<str:enqueteur_id>', views.staff_approve_profile,
                       name="staff_approve_profile"),
                  path('account_settings/', views.updateprofil, name='account_settings'),
                  path('delete_post/<str:post_id>', views.delete_post, name="delete_post "),
                  path('delete_form/<str:servey_id>', views.delete_form, name="delete_form "),
                  path('manage_mission', views.manage_mission, name="manage_mission"),

                  path('manage_post', views.manage_post, name="manage_post"),
                  path('manage_forms', views.manage_forms, name="manage_forms"),
                  path('IndexAdmin2/', views.IndexAdmin2, name='IndexAdmin2'),
                  path('tableau/', views.tableau, name='tableau'),
                  path('mailbox_read_enqueteur/<str:message_id>', views.mailbox_read_enqueteur, name='mailbox_read'),
                  path('mailbox_read_contact/<str:contact_id>', views.mailbox_read_contact, name='mailbox_read'),
                  path('builder/', views.builder, name='builder'),
                  path('sendx/', views.sendemail_confirmation, name='sendx'),

                  path('mailbox/', views.mailbox, name='mailbox'),
                  path('mailbox_compose/', views.mailbox_compose, name='mailbox_compose'),
                  path('mailbox_compose_envoie/<str:enqueteur_id>', views.mailbox_compose_envoie,
                       name='mailbox_compose_envoie'),
                  path('users_status/', views.users_status, name='users_status'),
                  path('sent/', views.sent, name='sent'),
                  path('servey/', views.servey, name='servey'),
                  path('createforms/', views.createforms, name='createforms'),
                  path('createforms/<str:mission>', views.buildpage, name='createforms'),
                  path('missiontest/', views.missiontest, name='missiontest'),
                  path('validation_visite/', views.validation_visite, name='validation_visite'),
    path('actualite/', views.actualite, name='actualite'),
    path('actualite_detail//<str:post_id>', views.actualite_detail, name='actualite_detail'),
    path('guide/', views.faq, name='guide'),
    path('contact/', views.contact, name='contact'),
                  path('contact_sent/', views.contact_sent, name='contact_sent'),
                  path('testx/', views.testx, name='testx'),
                  path('testxx/', views.testxx, name='testxx'),
                  path('testxxx/', views.testxxx, name='testxxx'),
                  path('mission_detail_apply/<str:post_id>', views.mission_detail_apply, name='mission_detail_apply'),
                  path('validationx/', views.validationx, name='validationx'),
                  path('delete_candidature/<str:candidature_id>', views.delete_candidature, name='delete_candidature'),
                  #path('verification/', include('verify_email.urls')),

                  path('mailbox_compose_envoie_save/', views.mailbox_compose_envoie_save, name='mailbox_compose_envoie_save'),
    path('profile/<str:enqueteur_id>', views.profile, name='profile'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('handicap/', views.handicap, name='handicap'),
    path('handicap_save', views.handicap_save, name='handicap_save'),
                  #Enqueteur
    path('indexoffre/', views.indexEnqueteur, name='indexEnqueteur'),
    path('contact_sent_enqueteur/', views.contact_sent_enqueteur, name='contact_sent_enqueteur'),
    path('trouveroffre/', views.Trouvermission, name='trouvermission'),
    path('mission_detail/<str:post_id>', views.mission_detail, name='mission_detail'),
    path('apply_for_mission/<str:mission_id>', views.apply_for_mission, name='apply_for_mission'),
    path('staff_apply_leave_save/', views.staff_apply_leave_save, name='staff_apply_leave_save'),
    path('offre/', views.mission, name='mission'),
    path('account_messages/', views.account_messages, name='account_messages'),
    path('account_payments/', views.account_payments, name='account_payments'),
    path('account_profile/', views.account_profile, name='account_profile'),
    path('updateprofile/', views.updateprofil, name='updateprofile'),
    path('article1/', views.article1, name='article1'),
    path('testte/', views.testte, name='testte'),
    path('article2/', views.article2, name='article2'),
    path('article3/', views.article4, name='article3'),
    path('article5/', views.article5, name='article5'),
    path('article4/', views.article3, name='article4'),
    path('demo/', views.dem, name='demo'),
    path('account_works/', views.account_works, name='account_works'),
    path('contact_enqueteur/', views.contact_enqueteur, name='contact_enqueteur'),
    path('createforms/', views.createforms, name='createforms'),
    path('createforms/<str:mission>', views.buildpage, name='createforms'),
    path('showdata/', views.showdata, name='showdata'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='Homepage/auth-re-password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='Homepage/auth-re-password1.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Homepage/auth-re-password2.html'),name='password_reset_confirm'),
    path('password_changed/', auth_views.PasswordResetCompleteView.as_view(template_name='Homepage/auth-re-password3.html'),name='password_reset_complete'),
                  path('testquestionnaire/', views.testquestionnaire, name='testquestionnaire'),
                  path('testm/', views.testm, name='testm'),

                  #Administrateur
    path('indexAdmin/', views.indexAdmin, name='IndexAdmin'),
    path('maps/', views.gpsmap, name='gpsmap'),
    path('getaverge/<str:mission>', views.getaverge, name='getaverge'),
    path('filterUserMission/<str:mission>/<str:user>', views.filterUserMission, name='filterUserMission'),
    path('gestion/', views.gestion, name='gestion'),
    path('test/', views.test, name='test'),
    path('testt/', views.testt, name='testt'),

                  path('terms/', views.terms, name='terms'),
                  path('text/', views.text, name='text'),
                  path('panel/', views.panel, name='panel'),

                  #mission et organisme

    path('showdata/', views.showdata, name='showdata'),
    path('data_each_mission', views.data_each_mission, name='data_each_mission'),
    path('approuve_survey/<str:id>', views.approuve_survey, name='approuve_survey'),
    path('refuse_survey/<str:id>', views.refuse_survey, name='refuse_survey'),
    path('remun_send/<str:id>', views.remun_send, name='remun_send'),
    path('refuse_remun/<str:id>', views.refuse_remun, name='refuse_remun')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

