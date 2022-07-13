from json.encoder import JSONEncoder
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
import json, random
from datetime import datetime, time
from django.urls import reverse

from .models import Resolutiondb, Incidentdb, StatusUpdatedb, Userdb

# Create your views here.
class WebApp():        
    def index(request):
        try:
            if request.session['username'] is not None:
            # populate table from db
                if request.method == 'GET':            
                    try:
                        incident_data = Incidentdb.objects.all()
                        # resolved_date = Admindb.objects.filter('resolved_date')
                        date_resolved = list()
                        #print("content available")
                        return render(request, 'RIT/index.html',  {'incidents':incident_data, 'resolved_date': date_resolved, 'username': request.session['username']})
                    except Incidentdb.DoesNotExist or Resolutiondb.DoesNotExist:
                        incident_data = []
                        date_resolved = []
                        return render(request, 'RIT/index.html',  {'incidents':incident_data, 'resolved_date': date_resolved, 'username': request.session['username']})
                else:
                    form_data = json.loads(request.body)
                    department = form_data['selected_department']
                    # print(department)
                    departmental_incident = Incidentdb.objects.filter(incident_department = department)
                    # print(departmental_incident)
                    return JsonResponse([dept.serialize() for dept in departmental_incident], encoder=JSONEncoder, safe=False) #, {'username': request.session['username']})
        except:
            # Exception as KeyError:
            #print(e)
            return render(request, 'RIT/login.html', {'message':"You've to login to report, review or resolve issues!"})

    def login(request):
        # get username from form and check db whether it exist and confirm password
        if request.method == 'POST':
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                try:                
                    check_username = Userdb.objects.all().filter(username=username, password=password)
                    request.session['username'] = username
                    username_session = request.session['username']
                    #print(username_session)
                    incidents = Incidentdb.objects.all()
                    if len(check_username) >= 1:                     
                        return HttpResponseRedirect(redirect_to='/RIT/')
                    else:
                        return render(request, 'RIT/login.html',  {'message':"username does not exist!"})
                except:
                    return render(request, 'RIT/login.html',{'message':"username or/and password is/are incorrect"})
            except:
                return render(request, 'RIT/login.html', {'message':"invalid parameters! Try again"})
        return render(request, 'RIT/login.html')

    def register(request):
        if request.method == 'POST':
            try:                
                admin_role = False
                username = request.POST.get('username')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                email = request.POST.get('email')
                department = request.POST.get('department')    
                role = request.POST.get('user_role')
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                if role == 'on':
                    admin_role = True
                else:
                    admin_role = False
                
                if password == confirm_password:
                    register_user = Userdb.objects.create(username=username, password=password, email=email, department=department, 
                        admin_role=admin_role, firstname=firstname, lastname=lastname)
                    return HttpResponseRedirect('/RIT/login/')
                else:
                    return render(request, 'RIT/register.html', {'message':"Confirm password should be the same as the password"})
                    # return render(request, 'RIT/login.html')
            except:
                return render(request, 'RIT/register.html', {'message':"User already exists!"})
        else:
            return render(request, 'RIT/register.html')

    def ticketno():
        rand_digits = random.randrange(1,1000000, 1)
        zeros = "0000000"
        ticket_number = ''
        if len(str(rand_digits)) < 7:
            ticket_number = zeros[:len(zeros)-len(str(rand_digits))] + str(rand_digits)        
        try: 
            check_incident_number = Incidentdb.objects.get(incident_ticket = ticket_number)
            if check_incident_number is not None:
                    ticket_number = WebApp.ticketno() 
            else:
                return ticket_number
        except Incidentdb.DoesNotExist:
            return ticket_number

    def incident_form(request):
        if request.method == 'POST':
                
            ticket_number = WebApp.ticketno()
            
            incident_department = request.POST.get('incident_department')
            incident_topic = request.POST.get('incident_topic')
            incident_date = request.POST.get('incident_date')
            # convert datetime format to proper string from ISO
            incident_date_time = datetime.fromisoformat(incident_date)
            incident_description = request.POST.get('incident_description')
            incident_priority = request.POST.get('incident_priority')
            incident_status = request.POST.get('incident_status')
            incident_ticket = ticket_number
            try:
                resolved_date = None
                username = Userdb.objects.get(username=request.session['username'])
                
                report_incident = Incidentdb.objects.create(username_id=username.username, incident_department=incident_department, incident_topic=incident_topic, 
                                incident_description=incident_description, incident_priority=incident_priority, incident_status=incident_status, 
                                    incident_ticket=incident_ticket, incident_date=incident_date_time)
                #print(username.username)
                return HttpResponseRedirect(redirect_to='/RIT/') 
                # render(request, 'RIT/index.html', {'username': request.session['username']})
            except:            
                return render(request, 'RIT/incidentForm.html', {'username':request.session['username']})           
        else:
            return render(request, 'RIT/incidentForm.html', {'username':request.session['username']})

    def dashboard(request):
        try:
            if request.session['username'] is not None:
            # populate table from db
                if request.method == 'GET':            
                    try:
                        incidents = Incidentdb.objects.all()
                        user_admin = Userdb.objects.get(username=request.session['username'])
                        date_resolved = list()
                        return render(request, 'RIT/dashboard.html', {'username': request.session['username'], 'incidents':incidents, 'user_admin':user_admin.admin_role})

                        #return render(request, 'RIT/index.html',  {'incidents':incident_data, 'resolved_date': date_resolved, 'username': request.session['username']})
                    except Incidentdb.DoesNotExist or Resolutiondb.DoesNotExist:
                        incidents = []
                        #date_resolved = []
                        return render(request, 'RIT/dashboard.html', {'username': request.session['username'], 'incidents':incidents})

                        #return render(request, 'RIT/index.html',  {'incidents':incident_data, 'resolved_date': date_resolved, 'username': request.session['username']})
                else:
                    form_data = json.loads(request.body)
                    department = form_data['selected_department']
                    departmental_incident = Incidentdb.objects.filter(incident_department = department)
                    
                    return JsonResponse([dept.serialize() for dept in departmental_incident], encoder=JSONEncoder, safe=False) #, {'username': request.session['username']})
            else:
                return render(request, 'RIT/login.html', {'message':"You've to login to report, review or resolve issues!"})
                   
        except:            
            return render(request, 'RIT/login.html', {'message':"You've to login to report, review or resolve issues!"})

    def dept_dashboard(request, department):
        if request.method == "GET":
            department = str.upper(department)
            incidents = Incidentdb.objects.filter(incident_department = department)
            #print(incidents)
            if (department is not None or department != '') and len(incidents) == 0:
                return render(request, 'RIT/dashboard.html', {'incidents':incidents, 'username': request.session['username']})
            return render(request, 'RIT/dashboard.html', {'incidents':incidents,  'department' : department, 'username':request.session['username']})
            # return HttpResponseRedirect(reverse('dept_dashboard', args = (department,)), {'incidents':incidents, 'username': request.session['username']})
        else:
            department = str.upper(department) # form_data['selected_department']
            departmental_incident = Incidentdb.objects.filter(incident_department = department)
           
            return render(request, 'RIT/dashboard.html', {'incidents':departmental_incident, 'username':request.session['username']})

# resolve/update incident status depending on selected status
    def resolve_incident(request):
        if request.method == 'POST':
            form_data = json.loads(request.body)

            incident_status = form_data['incident_status']
            incident_status_update = form_data['incident_resolution']
            incident_topic = form_data['incident_topic']
            incident_ticket_no = form_data['incident_ticket']
            
            # print(incident_ticket)
            username = request.session['username']

            # when status update is pending
            if incident_status == "Pending":
                # call the StatusUpdatedb
                #incident_ticket = Incidentdb.objects.get(incident_ticket=incident_ticket_no)
                update_incident = StatusUpdatedb.objects.create(username_id = username, incident_id = incident_ticket_no, incident_status_update = incident_status_update, 
                        update_date = datetime.now())
                incidents = Incidentdb.objects.all()
                return render(request, 'RIT/dashboard.html', {'incidents':incidents, 'username': request.session['username']})

            # when status update is resolved
            elif incident_status == "Resolved":
                incident_ticket = Incidentdb.objects.get(incident_ticket = incident_ticket_no) 
                resolved_date = datetime.now()
                resolve_incident = Resolutiondb.objects.create(ticket_number_id = incident_ticket_no, user_admin_id=username, incident_topic = incident_ticket.incident_topic, incident_resolution=incident_status_update,
                resolution_status = incident_status, report_date = incident_ticket.incident_date, resolved_date=resolved_date)
                
                # call the resolvedb/Admindb
                # date_resolved = Admindb.objects.get(username_id=username, resolve_date='')
                incident_ticket.incident_status = incident_status
                incident_ticket.incident_resolved_date = resolved_date
                incident_ticket.incident_resolution = incident_status_update
                incident_ticket.save()

                # pull all incidents with resolutions
                incidents = Incidentdb.objects.all()
                resolutions = Resolutiondb.objects.all()
                #print(resolutions)

                return render(request, 'RIT/dashboard.html', {'incidents':incidents, 'resolutions':resolutions, 'username': request.session['username']})
            else:
                incidents = Incidentdb.objects.all()
                return render(request, 'RIT/dashboard.html', {'incidents':incidents, 'username': request.session['username']})

    def update_incident(request):
        if request.method == 'POST':
            # collect form data``
            form_data = json.loads(request.body)  
            incident_status = form_data['incident_status']
            incident_status_update = form_data['incident_resolution']
            incident_topic = form_data['incident_topic']
            incident_ticket_no = form_data['incident_ticket']
            username = request.session['username']
            print("form data", form_data)
        pass

    def incident_status(request):
        if request.method == 'POST':
            print("post req: incident status")
            form_data = json.loads(request.body)
            incident_ticket_no = form_data['incident_ticket']
            print("value: ", incident_ticket_no)
            incident_ticket = Incidentdb.objects.get(incident_ticket = incident_ticket_no)
            return JsonResponse({"incident_status":incident_ticket.incident_status}, status=200)

        if request.method == 'GET':
            print("get req: incident status")
            incident_status = StatusUpdatedb.objects.all()
            return JsonResponse({"incident_status":incident_status}, status=200)
            
    def logout(request):
        request.session['username'] = None
        return HttpResponseRedirect(redirect_to='/RIT/login/')
