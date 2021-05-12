from django.urls import path

from . import views

app_name = 'welcome'
urlpatterns = [

	# le chemin welcome/ conduit à la page à la fonction login dans views
	path('', views.index, name = "index"),
	# le chemin welcome/login conduit à la page à la fonction login dans views
	path('login', views.login2, name = "login"),

	path('signout', views.signout, name = "signout"),

	path('add_friend', views.add_friend, name = "add_friend"),

	path('modif_profil', views.modif_profil, name = "modif_profil"),

	path('show_profil', views.show_profil, name = "show_profil"),

	path('register', views.register, name = "register")
]
