from django.shortcuts import render, redirect
from django.http import HttpResponse,  HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from welcome.forms import *
from welcome.models import *
from datetime import date

# Create your views here.



def get_logged_user_from_request(request):
	
	if request.user.is_authenticated:
		id_user =  request.user.id

		if len(Student.objects.filter(id = id_user)) == 1 :
			return Student.objects.get(id = id_user)

		elif len(Employee.objects.filter(id = id_user)) == 1:
			return Employee.objects.get(id = id_user)

		else:
			return None

	else:
		return None


def index(request):

	logged_person = get_logged_user_from_request(request)
	# return render(request, '<p> bonjour</p>')

	if logged_person:

		if 'newMessage' in request.GET and request.GET['newMessage'] != '' :
			nouveauMess = Message(author = request.user , content = request.GET['newMessage'] , publication_date = date.today())
			nouveauMess.save()
		

		friendsMessages = Message.objects.filter(author__friends = request.user).order_by('-publication_date')

		return render(request, 'welcome/index.html', {"logged_person": logged_person,
													"friendsMessages": friendsMessages})
	else :
		return HttpResponseRedirect(reverse('welcome:login',))


def login2(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('welcome:index'))
		# return render(request, 'welcome/index.html')

	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)

		if user is not None:
			# print('yessssssssssssssssssssssssssssssssss')
			login(request, user)
			return HttpResponseRedirect(reverse('welcome:index',))

		else:
			# a revoir
			return render(request, 'welcome/login.html')


	else:
		return render(request, 'welcome/login.html')

	# if len(request.POST) > 0:
		
	# 	email = request.POST['email']
	# 	password = request.POST['password']
	# 	user = authenticate(request, email=email, password=password)
	# 	login(request, user)
	# 		email_user = form.cleaned_data['email']
	# 		logged_user = UserProfile.objects.get(email = email_user)
	# 		request.session['logged_user_id'] = logged_user.id
	# 	return HttpResponseRedirect(reverse('welcome:index',))
	# 	else :
	# 		return render(request, 'welcome/login.html', {"form" : form})


	# else:
	# 	form = LoginForms()
	# 	return render(request, 'welcome/login.html', {"form" : form})

	# if len(request.POST) > 0:
	# 	# Test si les paramétres transmis on été envoyé
	# 	if "email" not in  request.POST or 'password' not in request.POST :
	# 		error = "Veillez remplir tous les champs"
	# 		return render(request, 'welcome/login.html', {'error':error})
	# 	else:
	# 		email = request.POST["email"]
	# 		password = request.POST["password"]
	# 		print(request.POST)
	# 		# On teste si le mot de passe et l'email sont bons
	# 		if password != "nanojunior92" and email != "onanadonald@gmail.com":
	# 			error = "Mot de passe ou email erroné"
	# 			return render(request, 'welcome/login.html', {'error': error})
	# 		# Sinon tou est bon on vas à la page d'acceuil
	# 		else:
	# 			return render(request, 'welcome/index.html')

	# # sinon le formulaire n'a pas encore été envoyé
	# else:
	# 	return render(request, 'welcome/login.html')


def signout(request) :
	logout(request)
	return HttpResponseRedirect(reverse('welcome:login',))


def register(request):
	# On verifie si on a reçu une methode GET
	if len(request.GET) > 0 and 'profileType' in request.GET:
		# on creer les deux formulaires vide
		studentForm = StudentProfileForms(prefix = "st")
		employeeForm = EmployeeProfileForms(prefix = "em")
		# On verifie s'il sagit d'un formulaire etudiant
		if request.GET['profileType'] == 'student':
			studentForm = StudentProfileForms(request.GET, prefix = "st")
			# on verifie s'il est valide
			if studentForm.is_valid():
				# si oui on enregistre les informations et on redirige vers la page de login
				studentForm.save()
				return HttpResponseRedirect(reverse('welcome:login',))
		# On verifie s'il sagit d'un formulaire employee
		elif request.GET['profileType'] == 'employee':
			employeeForm = EmployeeProfileForms(request.GET, prefix = "em")
			# on verifie s'il est valide
			if employeeForm.is_valid():
				# si oui on enregistre les informations et on redirige vers la page de login
				employeeForm.save()
				return HttpResponseRedirect(reverse('welcome:login',))
		# le formulaire envoyé n'était pas valide alors on rafraichit la page avec le meme formulaire
		return render(request, 'welcome/user_profile.html', {"studentForm":studentForm ,
															"employeeForm": employeeForm})
	# Pas de methode GET donc aucun formulaire n'a ete soumis
	else:
		studentForm = StudentProfileForms(prefix = "st")
		employeeForm = EmployeeProfileForms(prefix = "em")
		return render(request, 'welcome/user_profile.html', {"studentForm":studentForm ,
															"employeeForm": employeeForm})



def add_friend(request):
	

	logged_person = get_logged_user_from_request(request)
	# return render(request, '<p> bonjour</p>')

	if logged_person:
		
		if request.method == 'POST':
			form = AddFriendForm(request.POST)

			if form.is_valid():
				new_friend_mail = form.cleaned_data["email"]
				new_friend = UserProfile.objects.get(email = new_friend_mail)
				logged_person.friends.add(new_friend)
				logged_person.save()
				return HttpResponseRedirect(reverse('welcome:index'))

			else:
				return render(request, 'welcome/add_friend.html' , {"form" : form})
		else:
			form = AddFriendForm()
			return render(request, 'welcome/add_friend.html' , {"form" : form})

	else:

		return HttpResponseRedirect(reverse('welcome:login',))


def modif_profil(request):
	
	logged_person = get_logged_user_from_request(request)

	if logged_person:
		
		if request.method == 'POST':
			
			if request.user.person_type == 'student':

				form = StudentProfileForms(request.POST, prefix = "st")

				if form.is_valid():

					form.save()
					return HttpResponseRedirect(reverse('welcome:index'))

				else:

					return render(request, 'welcome/modif_profil.html' , {"form" : form})


			elif request.user.person_type == 'Employee':

				form = EmployeeProfileForms(request.POST, prefix = "st")

				if form.is_valid():

					form.save()
					return HttpResponseRedirect(reverse('welcome:index'))

				else:

					return render(request, 'welcome/modif_profil.html' , {"form" : form})

		else:

			if request.user.person_type == 'student':

				form = StudentProfileForms(prefix = "st")
				return render(request, 'welcome/modif_profil.html', {"form":form})

			# a revoir
			elif request.user.person_type == 'generic':
			#######
				form = EmployeeProfileForms(prefix = "em")

				return render(request, 'welcome/modif_profil.html', {"form": form})




	else:

		return HttpResponseRedirect(reverse('welcome:login',))



def show_profil(request):


	if request.user.is_authenticated:
		id_user =  request.user.id

		if len(Student.objects.filter(id = id_user)) == 1 :
			user_to_show =  Student.objects.get(id = id_user)

		elif len(Employee.objects.filter(id = id_user)) == 1:
			user_to_show =  Employee.objects.get(id = id_user)

		return render(request, 'welcome/show_profile.html', {'user_to_show': user_to_show})

	else:
		return HttpResponseRedirect(reverse('welcome:login',))