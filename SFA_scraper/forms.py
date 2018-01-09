from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bingScraper.models import Profile
import datetime
from django.db import models
from googleScraper.models import Company


class SignUpForm(UserCreationForm):
    Choices = (('Analyst', 'Analyst'), ('Management', 'Management'), ('Searcher', 'Searcher'))
    Teams = (('SFA', 'SFA'), ('Arden Bay', 'Arden Bay'), ('Bradford Lane', 'Bradford Lane'), ('Crescent Peak','Crescent Peak'), ('Servan & Co','Servan & Co'), ('Vallatus','Vallatus'),
		('Monan', 'Monan'),('Oakbourne', 'Oakbourne'),('Estes Point', 'Estes Point'),('Klaxon', 'Klaxon'))
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    access_level = forms.ChoiceField(choices=Choices, required = True, label = 'Access Level')
    team = forms.ChoiceField(choices=Teams, required = True, label = 'Team Selection')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'access_level', 'team')
    def save_profile(self, commit = True):
        data = self.cleaned_data
        user = super(SignUpForm, self).save(commit=False)
        profile = Profile(user = user, access_level = data['access_level'], team = data['team'])
        if commit:
            profile.save()
        return profile


class SignInForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, help_text='Enter your username')
    password = forms.CharField(widget=forms.PasswordInput(),max_length=30, required=True, help_text='Enter your password')


class AddCompanyForm(forms.Form):
    name = forms.CharField(max_length=100, required = True, help_text = 'Enter the company name')
    state = forms.CharField(max_length=10, help_text = 'Optional', required = False)
    city = forms.CharField(max_length=10, help_text = 'Optional', required = False)
    zipcode = forms.CharField(max_length=10, help_text = 'Optional', required = False)
    url = forms.CharField(max_length=255, help_text = 'required', required = True)
    owner_Name = forms.CharField(max_length=100, help_text = 'Optional', required = False)
    owner_email = forms.EmailField(required = False)
    industry = forms.CharField(max_length=100, help_text = 'Optional', required = False)
    class Meta:
        model = Company
        fields = ('name', 'url', 'city','state', 'zip', 'owner_email', 'owner_Name','industry', 'datetime')

    def save(self):
        data = self.cleaned_data
        company = Company(name=data['name'],  url=data['url'], city=data['city'], state=data['state'],
                    zipcode=data['zipcode'], owner_email=data['owner_email'], owner_Name=data['owner_Name'], 
                    industry=data['industry'], datetime = datetime.datetime.now())
        company.save()

