from django.db import models
import datetime
from user.models import Profile
import uuid

# Create your models here.
class Appointment(models.Model):
	TIME_CHOICES = (
                    ('09:00:00', '09 AM'),
                    ('10:00:00', '10 AM'),
                    ('11:00:00', '11 AM'),
                    ('13:00:00', '01 PM'),
                    ('14:00:00', '02 PM'),
                    ('15:00:00', '03 PM'),
                    ('16:00:00', '04 PM') )

	# is it necessary to create a service model ?
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
	uid = models.UUIDField(max_length =250, blank=True, unique=True, default=uuid.uuid4)
	patient = models.ForeignKey(Profile, on_delete=models.CASCADE)
	service = models.CharField(max_length=250, blank=False, choices=CHOICES)
	date = models.DateField(blank=True, null=True)
	time = models.TimeField(default=datetime.time(00, 00))
	note = models.TextField(max_length=5000, blank=True)
	created_at = models.DateField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateField(auto_now=True, blank=True, null=True)

	has_perscription = models.BooleanField(default = False)
	is_firsttime =  models.BooleanField(default = True)

	def __str__(self):
		return self.patient.user.username +'-'+ self.service + '-' +str(self.created_at)

	class Meta: 
		ordering = ('date',)



# import from third party databases
class Perscription(models.Model):
	name = models.CharField(max_length=10, blank=True, unique=True)
	appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
	dose = models.CharField(max_length=100, blank=True)
	instruction = models.TextField(max_length=5000, blank=True)
	sideaffect = models.TextField(max_length=5000, blank=True)
	link = models.URLField(max_length = 2000) 

	def __str__(self):
		return self.name











