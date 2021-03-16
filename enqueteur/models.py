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
    profile_pic = models.FileField(blank=True, null=True)
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
    description=models.CharField(max_length=9000, blank=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.nameform

class SurveyData(models.Model):
    MEDIA_CHOICES7 = (
        ('0', 'Pending'),
        ('1', 'Accepter'),
        ('2', 'refuser'),
    )
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=250,blank=True)
    nameform = models.CharField(max_length=250, blank=True)
    date = models.CharField(max_length=250, blank=True)
    data=models.JSONField(max_length=9000, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visite_status = models.IntegerField(default=0, choices=MEDIA_CHOICES7)

    def __str__(self):
        return self.nameform

class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField()

    def __str__(self):
        return self.nom


class Actualite(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    photo=models.IntegerField(default=13)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.title

class Mission(models.Model):
    id = models.AutoField(primary_key=True)
    ref= models.IntegerField(blank=True, null=True)
    nom = models.CharField(max_length=100)
    organisme = models.ForeignKey(Organisme, on_delete=models.CASCADE)
    thematique=models.CharField(max_length=30)
    questionnaire = models.ForeignKey(CreateForms, on_delete=models.CASCADE, blank=True)
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


class Contact_enqueteur(models.Model):
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255,blank=True, null=True)
    feedback_reply=models.TextField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



class Contact_admin(models.Model):
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    class Meta:
        ordering=['created_at']


class Commentaire(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Actualite, on_delete=models.CASCADE, blank=True,null=True)
    nom = models.TextField()
    commentaire = models.TextField()
    post_id = models.ForeignKey(Actualite, on_delete=models.CASCADE, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Professional(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField()
    username=models.CharField(max_length=255,blank=True, null=True)
    password=models.CharField(max_length=255,blank=True, null=True)
    mission_id = models.ForeignKey(Mission, on_delete=models.CASCADE, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class avergedata(models.Model):
    id = models.AutoField(primary_key=True)
    namemission = models.CharField(max_length=250, blank=True)
    averges = models.JSONField(max_length=9000,blank=True, null=True)


'''' 
class MessageEnqueteurs(models.Model):
    id = models.AutoField(primary_key=True)
    enqueteur_id = models.ForeignKey(Enqueteur, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=255, default="")
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    #statut= models.Boole
    objects = models.Manager()
    
'''

''''



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Enqueteur.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.enqueteur.save()



'''
# Create your models here.