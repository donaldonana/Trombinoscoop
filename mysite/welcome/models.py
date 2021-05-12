from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.




class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, name, password=None):
        """create the new user profile"""
        if not email:
            raise ValueError("User most have an email adresse")

        # email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create and save superuser with given detail"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """database for user in the systeme"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registration_nummber = models.CharField(max_length = 30, blank = True)
    first_name = models.CharField(max_length = 20, blank = True)
    last_name = models.CharField(max_length = 20, blank = True)
    # email = models.EmailField(unique = True)
    phone_numbers = models.CharField(max_length = 20, blank = True)
#     # password = models.CharField(max_length = 20)
    friends = models.ManyToManyField("self", blank = True)
    faculty = models.ForeignKey("Faculty", on_delete = models.CASCADE, blank = True, null = True)
    person_type = 'generic'

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """retrieve the full name of the user"""
        return self.name

    def get_short_name(self):
        """retrieve the short name of the user"""
        return self.name

    def __str__(self):
        """ str speciel methode of UserProfile """
        return self.email

    

# class Person( UserProfile):
#     """docstring for Person."""

#     registration_nummber = models.CharField(max_length = 30)
#     first_name = models.CharField(max_length = 20)
#     last_name = models.CharField(max_length = 20)
#     birth_day = models.DateField()
#     # email = models.EmailField(unique = True)
#     phone_numbers = models.CharField(max_length = 20)
#     # password = models.CharField(max_length = 20)
#     friends = models.ManyToManyField("self", blank = True)
#     faculty = models.ForeignKey("Faculty", on_delete = models.CASCADE, blank = True)
#     person_type = 'generic'

#     def __str__(self):
#         return self.first_name +" "+ self.last_name


class Message(models.Model):
    """docstring for Message."""

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateField()

class Faculty(models.Model):
    """docstring for Faculty."""

    name = models.CharField(max_length = 20)
    color = models.CharField(max_length = 20)

    def __str__(self):
        return self.name


class Campus(models.Model):
    """docstring for Campus."""

    name = models.CharField(max_length = 20)
    adresse = models.CharField(max_length = 20)

class job(models.Model):
    """docstring for job."""

    title = models.CharField(max_length = 20)

class Cursus(models.Model):
    """docstring for Cursus."""

    title = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.title)

class Employee( UserProfile ):
    """docstring for Employee."""

    office = models.CharField(max_length = 20, blank = True)
    campus = models.ForeignKey(Campus, on_delete = models.CASCADE, blank = True)
    job = models.ForeignKey(job , on_delete = models.CASCADE, blank = True)
    person_type = 'employee'

class Student( UserProfile ):
    """docstring for Student."""

    cursus = models.ForeignKey(Cursus, on_delete = models.CASCADE, blank = True, null = True)
    year = models.IntegerField(blank = True, null = True)
    person_type = 'student'
