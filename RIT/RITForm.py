from django import forms
from django.db.models import fields
from .models import Userdb

class UserdbForm(forms.Form):
    class Meta:
        model = Userdb
        fields = ['username','password','email', 'department','role','firstname', 'lastname']