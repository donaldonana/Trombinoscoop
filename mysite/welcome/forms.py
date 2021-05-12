from django import forms
from welcome.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

class LoginForms(forms.Form):
	"""Creation d'un formulaire avec la bibliothèque forms"""

	email = forms.EmailField(label = "courriel")
	password = forms.CharField(label = "Mot de Passe", widget = forms.PasswordInput)

	def clean(self):
		cleaned_data = super( LoginForms , self).clean()
		email = cleaned_data.get("email")
		password = cleaned_data.get("password")
		user = authenticate( email=email, password=password)

		if user is  None :
			raise forms.ValidationError("email ou mot de pass erroné")

		return cleaned_data





class StudentProfileForms(UserCreationForm):
	"""docstring for StudentProfileForms."""

	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	name = forms.CharField(max_length=30, required=False, help_text='*')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta :
		model = Student
		fields = ('email', 'name', 'first_name' , 'year')
		


class EmployeeProfileForms(UserCreationForm):
	"""docstring for EmployeeProfileForms."""

	class Meta :
		model = Employee
		fields = ('email', 'name', 'first_name' ,'office', 'campus', 'job')


class AddFriendForm(forms.Form):
	"""docstring for AddFriends"""

	email = forms.EmailField(label = "courriel")


	def clean(self):

		cleaned_data = super( AddFriendForm , self).clean()
		email = cleaned_data.get("email")
		# password = cleaned_data.get("password")
		# user = authenticate( email=email, password=password)

		if email:
			result = UserProfile.objects.filter(email = email)

			if len(result) != 1:
				raise forms.ValidationError("email ou mot de pass erroné")




		return cleaned_data




	
		
