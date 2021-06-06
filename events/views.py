from typing import ContextManager
import events
from django.contrib import messages
import re 
import bcrypt
from django.shortcuts import render,redirect
from .models import *

#event methods1 
# def test(request):
#     e=Event.objects.all()
#     context={
#             'events': e,
#         }
#     return render(request,'event.html',context) 
def details(request,id):
    event=Event.objects.filter(id=id)
    e=event[0]
    context = {
        "user": Users.objects.get(id=request.session['id']),
        "event":e
    }
    return render(request,'details.html',context) 
# event methods that needs checking
def test(request):#def event
    user = Users.objects.get(id=request.session['id'])
     
    context = {
        "user": user,
        "all_events": Event.objects.exclude(attended_by=user).exclude(event_creator=user),
        'attended_events':Event.objects.filter(attended_by=user),
        
    }
    # print(context['events'])
    # print("_" * 30)
    return render(request, "event.html", context)

def add(request):#add an event
    '''
    errors = Event.objects.event_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            print(f"{key}: {value}")
            messages.error(request, value, extra_tags = key)
        return redirect('/event')
    else:
        Event.objects.create(title=request.POST['title'],date=request.POST['date'],description=request.POST['description'], event_creator=Users.objects.get(id=request.session["id"]))
        return redirect('/event')
    '''
    Event.objects.create(title=request.POST['title'],date=request.POST['date'],description=request.POST['description'], event_creator=Users.objects.get(id=request.session["id"]))
    return redirect('/event')


def views(request, id):
    event = Event.objects.get(id=id)
    attended = event.attended.all()
    is_attended= attended.filter(id=id)
    is_attended= False
    if event.attended.filter(id=request.user.id).exists():
            is_attended= True
    context = {
        "event": event,
        "users": attended,
        "is_attended": is_attended,
        "logged_user": Users.objects.get(id=request.session['id'])
    }
    return render(request, "detail.html", context)

def attended(request, id):
    event = Event.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    event.attended_by.add(user)
    return redirect('/event')



def unattend(request, id):
    event = Event.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    event.attended_by.remove(user)
    return redirect('/event') 

def cancel(request, id):
    event = Event.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    event.attended_by.remove(user)
    return redirect('/event') 


def delete(request, id):
    
    user=Users.objects.get(id=request.session['id'])
    if user in request.session:
        event= Event.objects.get(id=id,)
        event.delete()
        return redirect('/profile')
    else:
        return redirect('/profile')
    
def edit_details(request, id):
    event= Event.objects.get(id=id)
    context={
        'event':event
    }
    return render(request,'edit_details.html',context)
def save_details(request,id):
    event= Event.objects.get(id=id)
    event.title = request.POST['title']
    event.description = request.POST['description'] 
    event.save()
    return redirect('/profile')
#stop here
def add_event(request):
    event=Event.objects.create(title=request.POST["title"],date=request.POST["date"],description=request.POST["description"])

    return redirect("/event")

# def delete_event(request, id):
#     e=Event.objects.filter(id=id)
#     e.delete()
#     return redirect("/event")

# User methods
def index(request):
    if 'id' in request.session:
        return redirect('/profile')
    else:
        return render(request, 'login.html')


    
def login(request):
    user_email = request.POST['email']
    user= Users.objects.filter(email=user_email)
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            if 'name' not in request.session:
                request.session['first_name']= user[0].first_name
                request.session['last_name']= user[0].last_name
                request.session['id']= user[0].id 
                request.session['user_email']= user[0].email
                request.session['user_password']= user[0].password
            return redirect("/success/"+str(user[0].id))
        return redirect('/')
    return redirect('/')


def registration(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
    errors={}    
    if len(request.POST['first_name'])<2:
        errors["first_name"] = "first name should be at least 2 characters"

    if len(request.POST['last_name'])<2:
        errors["last_name"] = "last name should be at least 2 characters"

    if not EMAIL_REGEX.match(request.POST['email']):               
        errors['email'] = "Invalid email address!"

    if len(request.POST['password'] )<4:
        errors['password'] = "Short password"
    
    if request.POST['password']!= request.POST['confirm_password']:
        errors['confirm'] = "Not matching"

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/register")
    else:
        first = request.POST['first_name'] 
        last = request.POST['last_name']
        email = request.POST['email'] 
        password = request.POST['password'] 
        conf = request.POST['confirm_password']
        if password==conf:
            hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()           
            user=Users.objects.create(first_name=first,last_name = last, email = email , password=hash)
            
            if 'id' not in request.session:
                request.session['id']= user.id 
                request.session['first_name']=first
                request.session['last_name']=last
                request.session['user_email']=email
                request.session['user_password']=hash 
                return redirect("/success/"+str(user.id))
    
    return redirect('/register') 

            
    
def register(request):
    return render(request,'register.html')

def profile(request):
    if 'id' in request.session:
        user=Users.objects.get(id=request.session["id"])
        context={
            "user":user,
            "created_events": Event.objects.filter(event_creator=user),

        }
        return render(request,"profile.html",context)
    # else:
    #     id=request.session['id']
    #     return render(request,"profile.html")
    return redirect("/")
            
def logout(request):
    request.session.flush()
    return redirect('/')

def update(request):
    errors={}
    if request.method == 'POST' :
        x= Users.objects.get(id=request.session['id'])
        x.first_name = request.POST['first_name']
        x.last_name = request.POST['last_name']
        x.email = request.POST['email']
        x.save()
        new=request.POST['new_password'] 
        conf_new=request.POST['confirm_new_password'] 

        if x:
            if  new!=conf_new:
                errors['confirm'] = "Not matching"

            if len(new)<4:
                errors['password'] = "Short password"

            else:
                hash = bcrypt.hashpw(new.encode(), bcrypt.gensalt()).decode()
                Users.objects.update(password=hash)

            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request, value)

        return redirect(f'/success/{x.id}')
def success(request,id):
    user=Users.objects.get(id=id)
    request.session['first_name']=user.first_name
    request.session['last_name']=user.last_name
    request.session['email']=user.email
    
    return render(request,'profile.html')

def show(request):
        email=request.POST['email']
        show = Users.objects.filter(email=email),
        if 'last_name' in request.session :
            show.last_name=request.POST['last_name']    
        show.email = request.POST['email'],
        show.password = request.POST['password'],
        return render(request,"profile.html")


            # email=request.POST['email']
        # if request.method == 'POST' :
        #     profile_update = Users.objects.get(id=id)
        #     profile_update.first_name=request.POST['first_name']
        #     profile_update.last_name=request.POST['last_name'] 
        #     profile_update.email=request.POST['email'] 
        #     profile_update.password=request.POST['password']
        #     profile_update.save()
        #     return redirect('/profile')

def main(request):
    return render(request,'main.html')
