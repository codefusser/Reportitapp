from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.

class Userdb(models.Model):
    # username_id = models.IntegerField('id', 'id', auto_created=True, unique=True)
    username = models.CharField('username', 'username', max_length = 100, unique = True, primary_key=True)
    password = models.CharField('password', 'password', max_length = 100, primary_key = False, unique = False)
    email = models.EmailField('email', 'email', primary_key=False, max_length=100, unique= True, blank= True)
    department = models.CharField('department', 'department', False, max_length = 100)
    admin_role = models.BooleanField('admin_role', 'admin_role', default=False)
    firstname = models.CharField('firstname', 'firstname', max_length=100)
    lastname = models.CharField('lastname', 'lastname', max_length=100)
    

class Incidentdb(models.Model):
    username = models.ForeignKey(Userdb, on_delete=models.CASCADE)
    incident_department = models.CharField(max_length=100)
    incident_topic = models.CharField(max_length=100)
    incident_description = models.TextField('incident_description', blank=False)
    incident_priority = CharField(max_length=50)
    incident_status = CharField(max_length=20)
    incident_ticket = CharField(verbose_name='incident_ticket', name='incident_ticket', primary_key=True, unique=True, max_length=50)
    incident_resolution = models.TextField('incident_resolution', blank=True, null=True)
    incident_date = models.DateTimeField('incident_date', blank=False)
    incident_resolved_date = models.DateTimeField(name='incident_resolved_date', unique=False, null=True)

class Resolutiondb(models.Model):
    ticket_number = models.ForeignKey(Incidentdb, on_delete=models.CASCADE, to_field='incident_ticket')
    user_admin = models.ForeignKey(Userdb, on_delete=models.CASCADE)
    incident_topic = models.CharField(max_length=100)
    incident_resolution = models.TextField('incident_resolution', blank=False)
    resolution_status = CharField(max_length=20)
    report_date = models.DateTimeField('report_date', blank=False)
    resolved_date = models.DateTimeField('resolved_date', blank=False)

class StatusUpdatedb(models.Model):
    username = models.ForeignKey(Userdb, on_delete=models.CASCADE)
    incident = models.ForeignKey(Incidentdb, on_delete=models.CASCADE)
    incident_status_update = models.TextField('incident_status_update', blank=False)
    update_date = models.DateTimeField(blank=False)