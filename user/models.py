from __future__ import unicode_literals
 
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class Profile(models.Model):
	CHOICES = (
	    ("Depression", "Depression"),
	    ("ADHD", "ADHD"),
	    ("Autism", "Autism"),
	    ("Anxiety", "Anxiety"),
	    ("Bipolar", "Bipolar"),
	    ("Behavior", "Behavior"),
	    ("Eating Disorder", "Eating Disorder"),
	    ("Others", "Others"),
	)
	USER_GENDER = (
		('Male', 'Male'), 
		('Female', 'Female'),
		('Non Binary', 'Non Binary'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
	bio = models.TextField(max_length=5000, blank=True)
	address = models.CharField(max_length=30, blank=True)
	gender = models.CharField(max_length=10, choices=USER_GENDER, default='none')
	birth_date = models.DateField(null=True, blank=True)
	email_confirmed = models.BooleanField(default=False)
	concerns = models.CharField(max_length = 50, choices = CHOICES, blank=True)
	created_at = models.DateField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateField(auto_now=True, blank=True, null=True)
	

	def __str__(self):
		return self.user.username


class Appointment(models.Model):
	TIME_CHOICES = (
                    ('09:00:00', '09 AM'),
                    ('10:00:00', '10 AM'),
                    ('11:00:00', '11 AM'),
                    ('13:00:00', '01 PM'),
                    ('14:00:00', '02 PM'),
                    ('15:00:00', '03 PM'),
                    ('16:00:00', '04 PM') )
	patient = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
	token = models.IntegerField()
	date = models.DateField(blank=True, null=True)
	time = models.TimeField(null=True, blank=True, choices=TIME_CHOICES)
	note = models.TextField(max_length=5000, blank=True)
	created_at = models.DateField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return str(self.patient.username)

	class Meta: 

		ordering = ('date',)
          
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
