from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from django.utils import formats
from .models import User, Appointment
import bcrypt


def index(request):
	return render(request,'belt_app/index.html')


def register(request):
    Name = request.POST['Name']
    Alias = request.POST['Alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    context = {'Name': Name,'Alias': Alias, 'email': email, 'password': password, 'confirm_password': confirm_password}
    errors = User.objects.validate(context)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
		hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		user = User.objects.create(Name = Name, Alias = Alias, email = email, password = hashed_password )
		request.session['id'] = user.id
		return redirect("/appointments")

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    print "inside login"
    
    errors = User.objects.validateLogin(request.POST)
    print errors
    if errors:
        print "heres"
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print "redirecting to root"
        return redirect('/')
    else:
        user = User.objects.filter(email = email)[0]
        request.session['id'] = user.id
        return redirect("/appointments")

def logout(request):
    request.session['id'] = ""
    return redirect('/') 

def appointments(request):
	print "inside appointments"
	if 'id' in request.session:
		today=datetime.date.today()
		request.session['today'] = formats.date_format(today, 'DATE_FORMAT')
		#print "Date in appts", unicode(datetime.date.today())
		print "today date"
		appointments = Appointment.objects.filter(user_id=request.session['id'], date=unicode(datetime.date.today())).order_by("-time").reverse()
		print "inside date"
		other_appointments = Appointment.objects.filter(user_id=request.session['id']).exclude(date=unicode(datetime.date.today())).order_by("-date","-time").reverse()
	

		context = {
			"appointments": appointments,
			"other_appointments": other_appointments
		}
		return render(request, "belt_app/appointments.html", context)
	return redirect('/')

def add(request):
	if 'id' in request.session:
		print "Name present", request.session['id']
		user_id = request.session['id']
		appointment = Appointment.objects.appointment_valid(request.POST, user_id)
		if appointment[0] == False:
			for error in appointment[1]:
				messages.add_message(request, messages.INFO, error)
		else:
			print "In else"
			#user = Appointment.objects.create(task=task, time=time, date=date, status=status)
			return redirect('/appointments')
	return redirect('/appointments')





def users(request):
    
    context = {}
    theUser = User.objects.get(id = number)
    
    return render(request, 'belt_app/appointments.html', context)



def delete(request, number):
	Appointment.objects.get(id=number).delete()
	return redirect("/appointments")
	

def edit(request, number):

	appointment = Appointment.objects.get(id = number)
	context = {
		"appointment": appointment
	}
	#user_id = request.session['id']
	
	return render(request, 'belt_app/update.html',context)

def update(request, number, id):

	result= Appointment.objects.update_app(request.POST, number, id)
	# user_id = request.session['id']
	# appointment = Appointment.objects.appointment_valid(request.POST, user_id)
    
	# appointment.save()
	if result[0] == False:
		for error in result[1]:
			messages.add_message(request, messages.INFO, error)
	else:
		return redirect("/appointments")

	return redirect("/update")