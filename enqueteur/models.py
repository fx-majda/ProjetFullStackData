from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
import os

class Enqueteur(models.Model):
    MEDIA_CHOICES2 = (
        ('1', 'oui'),
        ('2', 'non'),
    )
    MEDIA_CHOICES = (
        ('1', 'Homme'),
        ('2', 'Femme'),
    )
    MEDIA_CHOICES2 = (
        ('1', 'oui'),
        ('2', 'non'),
    )
    MEDIA_CHOICES5 = (
        ('1', 'Maison'),
        ('2', 'Appartement'),
        ('3', 'Villa'),
        ('4', 'Lotissement'),
        ('5', 'Autre'),

    )
    MEDIA_CHOICES4 = (
        ('1', 'Entre 0 et 3'),
        ('2', 'Entre 3 et 6'),
        ('3', 'Plus de 6'),
    )
    MEDIA_CHOICES7 = (
        ('1', '8h00 - 12h00'),
        ('2', '12h00 - 14h00'),
        ('3', '14h00 - 17h00'),
    )
    MEDIA_CHOICES6 = (
        ('1', 'Proprietaire'),
        ('2', 'locataire'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=20,null=True,blank=True)
    genre = models.CharField(max_length=25, null=True)
    telephone = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    adresse = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    birth_day = models.DateTimeField(blank=True, null=True)
    created_at = models.CharField(blank=True, max_length=250)
    ordinateur = models.CharField(max_length=25, choices=MEDIA_CHOICES2, blank=True)
    vehicule = models.CharField(max_length=25, choices=MEDIA_CHOICES2, blank=True)
    userexpen = models.CharField(max_length=40, blank=True, null=True)
    userexp = models.CharField(max_length=40, blank=True, null=True)
    expmois = models.CharField(max_length=25, choices=MEDIA_CHOICES4, blank=True, null=True)
    societe = models.CharField(max_length=40, blank=True, null=True)
    lunettes = models.CharField(max_length=25, choices=MEDIA_CHOICES2, blank=True, null=True)
    logement = models.CharField(max_length=40, choices=MEDIA_CHOICES6, blank=True, null=True)
    habitation = models.CharField(max_length=40, choices=MEDIA_CHOICES5, blank=True, null=True)
    langues = models.CharField(max_length=40,null=True,blank=True)
    meilleur = models.CharField(max_length=40, blank=True, null=True)
    pire = models.CharField(max_length=40, blank=True, null=True)
    restaurant = models.CharField(max_length=25, choices=MEDIA_CHOICES4, blank=True, null=True)
    situation = models.CharField(max_length=40, blank=True, null=True)
    profile_pic = models.FileField(upload_to='photos/',blank=True, null=True)
    joindre = models.CharField(max_length=25, choices=MEDIA_CHOICES7, blank=True, null=True)
    enfants = models.CharField(max_length=25, choices=MEDIA_CHOICES4, blank=True, null=True)
    status = models.BooleanField()

    def __str__(self):
        return self.nom


class Organisme(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20)
    photo=models.ImageField(blank=True, null=True,upload_to='media/mission_logo')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


    def __str__(self):
        return self.nom


class CreateForms(models.Model):
    id = models.AutoField(primary_key=True)
    nameform = models.CharField(max_length=250, blank=True)
    coreform = models.CharField(max_length=9000, blank=True)
    organisme=models.ForeignKey(Organisme, on_delete=models.CASCADE)
    description=models.CharField(max_length=9000, blank=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.nameform

class SurveyData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=250, blank=True)
    nameform = models.CharField(max_length=250, blank=True)
    date = models.CharField(max_length=250, blank=True)
    data=models.JSONField(max_length=9000, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nameform

class Actualite(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    keywords = models.TextField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

class Mission(models.Model):
    id = models.AutoField(primary_key=True)
    ref= models.IntegerField(blank=True, null=True)
    nom = models.CharField(max_length=100)
    organisme = models.ForeignKey(Organisme, on_delete=models.CASCADE)
    thematique=models.CharField(max_length=30)
    questionnaire = models.ForeignKey(CreateForms, on_delete=models.CASCADE)
    remuneration=models.CharField(max_length=40)
    description=RichTextField()
    date_debut= models.DateField(blank=False)
    date_fin= models.DateField(blank=False)
    ville = models.CharField(max_length=20)
    pays = models.CharField(max_length=20)
    objects = models.Manager()

    def __str__(self):
        return self.nom

class Candidature(models.Model):
    MEDIA_CHOICES7 = (
        ('0', 'Pending'),
        ('1', 'Accepter'),
        ('2', 'refuser'),
    )
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    mission_id = models.ForeignKey(Mission, on_delete=models.CASCADE)
    candidature_status = models.IntegerField(default=0, choices=MEDIA_CHOICES7)
    motivation = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255,blank=True, null=True)
    comments = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



''''

class Enqueteur(models.Model):
    MEDIA_CHOICES = (
        ('1', 'Homme'),
        ('2', 'Femme'),
    )
    MEDIA_CHOICES2 = (
        ('1', 'oui'),
        ('2', 'non'),
    )
    MEDIA_CHOICES5 = (
        ('1', 'Maison'),
        ('2', 'Appartement'),
        ('3', 'Villa'),
        ('4', 'Lotissement'),
        ('5', 'Autre'),

    )
    MEDIA_CHOICES4 = (
        ('1', 'Entre 0 et 3'),
        ('2', 'Entre 3 et 6'),
        ('3', 'Plus de 6'),
    )
    MEDIA_CHOICES7 = (
        ('1', '8h00 - 12h00'),
        ('2', '12h00 - 14h00'),
        ('3', '14h00 - 17h00'),
    )
    MEDIA_CHOICES6 = (
        ('1', 'Proprietaire'),
        ('2', 'locataire'),
    )
    CHOICES=(
        ('1', 'Verified'),
        ('2', 'unverified'),
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=25,choices=CHOICES)
    profile_pic = models.FileField(blank=True, null=True)
    nom = models.CharField(max_length=40,blank=True, null=True)
    gender = models.CharField(max_length=25,choices=MEDIA_CHOICES)
    tel = models.IntegerField( blank=True, null=True)
    ordinateur = models.CharField(max_length=25,choices=MEDIA_CHOICES2,blank=True)
    vehicule = models.CharField(max_length=25,choices=MEDIA_CHOICES2,blank=True)
    userexpen = models.CharField(max_length=40,blank=True)
    userexp= models.CharField(max_length=40,blank=True)
    expmois=models.CharField(max_length=25,choices=MEDIA_CHOICES4,blank=True)
    societe= models.CharField(max_length=40,blank=True)
    lunettes= models.CharField(max_length=25,choices=MEDIA_CHOICES2,blank=True)
    logement=models.CharField(max_length=40,choices=MEDIA_CHOICES6,blank=True)
    habitation=models.CharField(max_length=40,choices=MEDIA_CHOICES5,blank=True)
    langues= models.CharField(max_length=40,blank=True)
    meilleur= models.CharField(max_length=40,blank=True)
    pire= models.CharField(max_length=40,blank=True)
    restaurant=models.CharField(max_length=25,choices=MEDIA_CHOICES4,blank=True)
    situation= models.CharField(max_length=40,blank=True,null=True)
    joindre=models.CharField(max_length=25,choices=MEDIA_CHOICES7,blank=True)
    enfants=models.CharField(max_length=25,choices=MEDIA_CHOICES4,blank=True)
    motivation = models.TextField(max_length=500, blank=True, null=True)
    adresse = models.TextField(max_length=500, blank=True, null=True)
    city = models.TextField(max_length=500, blank=True, null=True)
    zipcode = models.IntegerField( blank=True, null=True)
    country = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Professional(models.Model):
        id = models.AutoField(primary_key=True)
        nom = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        objects = models.Manager()




class Organisme(models.Model):
    id = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Mission(models.Model):
    id = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=20)
    organisme = models.CharField(max_length=30)
    date_debut= models.DateField(blank=False)
    date_fin= models.DateField(blank=False)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)
    #location = models.PointField()
    objects = models.Manager()


class Questionnaire(models.Model):
    id= models.AutoField(primary_key=True)
    questions=models.CharField(max_length=100, blank=False)
    objects = models.Manager()


class MessageEnqueteurs(models.Model):
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=255, default="")
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    #statut= models.Boole
    objects = models.Manager()


class NotificationEnqueteurs(models.Model):
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Candidature(models.Model):
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    candidature_date = models.CharField(max_length=255)
    reply_message = models.TextField()
    candidature_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Enqueteur.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.enqueteur.save()



'''
# Create your models here.