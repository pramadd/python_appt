from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
import datetime



class UserManager(models.Manager):
    def validate(self, postData):
		errors = {}
		my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData['Name']) < 3:
			errors['Name'] = "Name  must be at least 3 characters"

		if len(postData['Alias']) < 1:
			errors['Alias'] = "Alias  must be at least 1 characters"

		if not my_re.match(postData['email']):
			errors['email'] = " enter a valid email id"

		if postData['password'] != postData['confirm_password']:
			errors['password'] = "passwords must match"

		return errors
        # min_age = 24
        # max_date = date.today()
        # try:
        #     max_date = max_date.replace(year=max_date.year - min_age)
        # except ValueError: # 29th of february and not a leap year
        #     assert max_date.month == 2 and max_date.day == 29
        #     max_date = max_date.replace(year=max_date.year - min_age, month=2, day=28)
        # people = People.objects.filter(birth_date__lte=max_date)

    def validateLogin(self, postData):
		errors = {}
		my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		hash2 = postData['password'].encode()
       
		if not my_re.match(postData['email']):
			errors['email'] = "Enter a valid email id"
		else :
            # try:
			try :
				user = User.objects.get(email = postData['email'])
				print "user  "
				if (user):
					if bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
						print "logged in"
					else :
						errors['password'] = "password do not match"          
			except :
				# User.DoesNotExist:
				errors['emailnotexist']="email doesn't exist"
				print "user not found"        
		print errors
		return errors

class AppointmentManager(models.Manager):
	def appointment_valid(self, POST, user_id):
		print "AppManager", user_id
		user_id = user_id
		task = POST['task']
		date = POST['date']
		time = POST['time']
		#status = POST['status']
		errors = []
		
		if len(task) < 1 or len(date) < 1 or len(time) < 1:
			errors["mesage"]="A field can not be empty"
		else:
			if date < unicode(datetime.date.today()):
				errors["date"]="Appointment can not be in the past"
			else:
				#user = User.objects.get(id=user_id)
				appointment = Appointment.objects.create(user_id=user_id, task=task, date=date, time=time)
				return (True, appointment)
		return (False, errors)


	def update_app(self, POST,user_id , row_id):
		new_task = POST['task']
		new_status = POST['status']
		new_date = POST['date']
		new_time = POST['time']
		errors = []

		if len(new_task) < 1 or len(new_date) < 1 or len(new_time) < 1 or len(new_status) < 1:
			errors["message"]="A field can not be empty"
		else:
			if new_date < unicode(datetime.date.today()):
				errors["new_date"]="A date can not be in the past"
			else:
				appointment = Appointment.objects.filter(user_id=user_id, id=row_id).update(task=new_task, status = new_status, date=new_date, time=new_time)
				return (True, appointment)
		return (False, errors)

class User(models.Model):
    Name = models.CharField(max_length = 255)
    Alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.name, self.alias, self.email, self.password)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.name, self.alias, self.email, self.password)



class Appointment(models.Model):
   	#user= models.CharField(max_length = 255)
	task = models.CharField(max_length = 255)
	time = models.TimeField(null=False)   
	date = models.CharField(max_length=255)
	status = models.CharField(max_length=255, default="Pending")
	user = models.ForeignKey(User, related_name="appointments")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = AppointmentManager()
	def __repr__(self):
		return "Appointment: \n{}\n{}\n{}\n{}\n".format (self.task, self.time,self.date,self.status)
	def __str__(self):
		return "Appointment: \n{}\n{}\n{}\n{}\n".format(self.task, self.time,self.date,self.status)