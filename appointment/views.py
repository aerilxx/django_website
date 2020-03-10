from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


from user.models import Profile
from .models import Appointment, Perscription
from .forms import  AppointmentForm , UpdateAppointmentForm
import datetime

from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from twilio.rest import Client


def broadcast_sms(request, recipient, msg):
   
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=recipient,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)


@login_required
def manage_appointment(request):
	user = request.user
	patient = Profile.objects.get(user=user)
	appointments = Appointment.objects.filter(patient=patient)

	if not appointments:
		return render(request, 'appointment/no_appointment.html')

	return render(request, 'appointment/index.html', {'appointments':appointments})



# initial appoitment 
@login_required
def make_appointment(request):
	user = request.user
	patient = Profile.objects.get(user=user)
	appointmentForm=''

	if not (user and user.is_active):
		return render(request, 'message/error.html',{'err':'Please activate your account.'})	

	if request.method == "POST":
		appointmentForm = AppointmentForm(request.POST)
		if appointmentForm.is_valid():
			app = appointmentForm.save(commit=False)
			app.patient = patient
			app.service = appointmentForm.cleaned_data['service']
			app.is_firsttime = False
			app.save()
			# msg = ("You have sucessfully make an appointment with Dr Zhou.")
			# broadcast_sms(request, patient.phone, msg)
			msg = "You have made an appointment!"
			messages.add_message(request, messages.SUCCESS, msg)
			return redirect('appointment_index')
	
		else:
			print(appointmentForm.errors)
			messages.add_message(request, messages.ERROR, appointmentForm.errors)
			print('form invalid')

	else:
		appointmentForm = AppointmentForm(request.POST)

	return render(request, 'appointment/make.html',{'form':appointmentForm})


@login_required
def view_appointment(request, appointment_id):
	user = request.user
	patient = Profile.objects.get(user=user)
	appointment=get_object_or_404(Appointment, id= appointment_id)
	if not (user.is_active and patient == appointment.patient):
		return render(request, 'message/error.html',{'err':"You don't have the "
			"permission to view this appointment."})	

	return render(request, 'appointment/view.html',{'appointment': appointment})


@login_required
def update_appointment(request, appointment_id):
	user = request.user
	patient = Profile.objects.get(user=user)
	appointment=get_object_or_404(Appointment, id= appointment_id)	
	context={}

	if not (user.is_active and patient == appointment.patient):
		return render(request, 'message/error.html',{'err':"You don't have the permission to update this appointment."})	

	appointmentForm = UpdateAppointmentForm(request.POST or None, instance= appointment)
	dt = datetime.datetime.combine(appointment.date, appointment.time)

	if dt <= datetime.datetime.now():
		msg = "You cannot edit past appointment!"
		messages.add_message(request, messages.ERROR, msg)

	elif request.method == "POST":
		if appointmentForm.is_valid():
			app = appointmentForm.save(commit=False)
			print('form valid, but not sure it saved' )
			app.save()
			msg = "You have successfully updated the appointment time."
			broadcast_sms(request, patient.phone, msg)
			messages.add_message(request,  messages.SUCCESS, msg)
			context= {'form': appointmentForm}
			return redirect('appointment_index')
		else:
			messages.add_message(request, messages.ERROR, "There is something wrong.")
		
	else:
		context= {'form': appointmentForm,
                  'error': 'The time was not updated.'}

	return render(request, 'appointment/update.html', context)



@login_required
def delete_appointment(request, appointment_id):
	user = request.user
	patient = Profile.objects.get(user=user)
	appointment=get_object_or_404(Appointment, id= appointment_id)
	if not (user.is_active and patient == appointment.patient):
		return render(request, 'message/error.html',{'err':"You don't have the "
			"permission to update this appointment."})	

	dt = datetime.datetime.combine(appointment.date, appointment.time)

	if dt <= datetime.datetime.now():
		msg = "You cannot cancel past appointment!"
		messages.add_message(request, messages.ERROR, msg)

	else:
		appointment.delete()
		msg = "You have cancel this appointment!"
		messages.add_message(request, messages.SUCCESS, msg)

	return redirect('appointment_index')


