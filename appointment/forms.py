from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import Appointment, Perscription
import datetime


class AppointmentForm(ModelForm):
	CHOICES = CHOICES = (
	    ("Depression", "Depression"),
	    ("ADHD", "ADHD"),
	    ("Autism", "Autism"),
	    ("Anxiety", "Anxiety"),
	    ("Bipolar", "Bipolar"),
	    ("Behavior", "Behavior"),
	    ("Eating Disorder", "Eating Disorder"),
	    ("Others", "Others"),
	)
	HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(9, 15)]

	service = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

	class Meta:	
		HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(9, 15)]

		model = Appointment 
		fields = (
			"date",
			"time",
			# "service",
			"note",
			'is_firsttime'
	     )
		widgets = {
            "time": forms.Select(choices=HOUR_CHOICES,attrs={'class':'ui-select'}),
        }

	def check_available(self,datetime):
		# list of dic
		appointment = Appointment.objects.all()
		date_list=[]
		for each in appointment:
			dt = datetime.combine(each.date, each.time)
			date_list.append(dt)

		if datetime in date_list:
			print('time slot taken')
			return 'unavailable'

		return "available"


# if time slot is already exist in db, don't allow user to take the slot
	def clean(self):
		super(AppointmentForm, self).clean() 
          
        # extract the date and time field from the data 
		date = self.cleaned_data.get('date') 
		time = self.cleaned_data.get('time') 
		cur_time = datetime.datetime.now()
	
		if date and time:
			dt = datetime.datetime.combine(date, time)

        # conditions to not allow user book the appointment		
			if dt <= cur_time:
				self._errors['date'] = self.error_class([ 
                'You cannot make an appointment earlier than current time.']) 

			if self.check_available(dt) == 'unavailable':
				self._errors['date'] = self.error_class([ 
                'This time slot is not available']) 

        # return any errors if found 
		return self.cleaned_data 

class UpdateAppointmentForm(ModelForm):
	class Meta:	
		HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(9, 15)]

		model = Appointment 
		fields = (
			"date",
			"time",
	     )
		widgets = {
            "time": forms.Select(choices=HOUR_CHOICES,attrs={'class':'ui-select'}),
        }


