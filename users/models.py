from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    person = models.CharField(max_length=100, null=True)
    bio = models.TextField(null=True)
    skills = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(upload_to='profile_pic', blank=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=15, null=True)



    def __str__(self):
        return self.user.username

class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)

    # Add other fields as needed

    def __str__(self):
        return self.title

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.company_name

class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.institution

class Certification(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    # Add other fields as needed

    def __str__(self):
        return self.title



# Create your models here.
