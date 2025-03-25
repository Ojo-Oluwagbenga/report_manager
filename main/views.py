from django.shortcuts import render
from django.shortcuts import redirect
import json
from .models import *
# Create your views here.

def only_logged_outs(v_method):
    def wrap(response):
        if response.session.get("user_data"):
            return redirect("/dashboard")
        else:
            return v_method(response)
    return wrap

@only_logged_outs
def login(response):
    return render(response, "login.html", {})


def dashboard(response):
    try:
        if not response.session.get("user_data"):
            response.session.flush()
            return redirect("/login")
                
        #UPDATE THE USER KEY EXPIRY SINCE USER IS ACTIVE
        response.session.set_expiry(864000) #SHIFTS TO 10 DAYS FROM NOW
        user_code = response.session['user_data'].get("user_code")

        user_set = User.objects.filter(user_code=user_code)
        u_data = user_set[0]

        if u_data.questionaire:
            if u_data.questionaire.get('status') != 'filled':
                return redirect("/questionaire")
        else:
            return redirect("/questionaire")

        qset = {
            "user_data":response.session['user_data'],
            "name":response.session['user_data']['name'],
            "schedule":json.dumps(u_data.schedule),
        }

        return render(response, "dashboard.html", qset)

    except Exception as e:
        print (e)
        response.session.flush()
        return redirect("/login")

def report(response, report_code):
    if not response.session.get("user_data"):
        response.session.flush()
        return redirect("/login")
            
    #UPDATE THE USER KEY EXPIRY SINCE USER IS ACTIVE
    response.session.set_expiry(864000) #SHIFTS TO 10 DAYS FROM NOW
    user_code = response.session['user_data'].get("user_code")
    user_set = User.objects.filter(user_code=user_code)
    
    #EXTRACT ALL THE USER THAT CAN BE APPENDABLE
    users = User.objects.filter(user_type='supervisee')
    data = list(users.values('email'))  
    dlist = []
    for usr in data:
        if (usr['email'] != response.session['user_data'].get("email")):
            dlist.append(usr['email'])
    dlist = sorted(dlist)  # Returns a new sorted list
            
    u_data = user_set[0]
    
    qset = {
        'report_data':u_data.schedule[report_code],
        'report_code':report_code,
        'users':json.dumps(dlist)
    }
    print (qset)

    return render(response, "report.html", qset)

def questionaire(response):
    if not response.session.get("user_data"):
        response.session.flush()
        return redirect("/login")
            
    #UPDATE THE USER KEY EXPIRY SINCE USER IS ACTIVE
    response.session.set_expiry(864000) #SHIFTS TO 10 DAYS FROM NOW
    user_code = response.session['user_data'].get("user_code")
    user_set = User.objects.filter(user_code=user_code)

    u_data = user_set[0]

    if u_data.user_type == 'supervisor':
        return render(response, "questionaire_supervisor.html", {})
    else:
        return render(response, "questionaire_supervisee.html", {})


def join_report(response, user_code, inviter_code, report_code):
    report_code = str(report_code)
    user_set = User.objects.filter(user_code=user_code)
    user_set2 = User.objects.filter(user_code=inviter_code)
    u_data = user_set[0]
    u_data2 = user_set2[0]

    if u_data.schedule.get(report_code):
        return redirect("/report/" + report_code)

    u_data.schedule[report_code] = {
        "partner":u_data2.email, 
        "partner_type":u_data2.user_type,
        "draft":"",
        "status":"unsaved", 
        "new_time":u_data2.schedule[report_code]['new_time']
    }
    u_data.save()
    return redirect("/report/" + report_code)
    


def logout(response):
    response.session.flush()
    return redirect("/login")
