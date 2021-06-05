from django.contrib import messages
import re 
import bcrypt
from django.shortcuts import render,redirect
from .models import *

def index(request):
    if 'id' in request.session:
        return redirect('/profile')
    else:
        return render(request, 'login.html')
# Create your views here.

    
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
        }
        return render(request,"profile.html",context)
    else:
        return redirect("/")
            
def logout(request):
    request.session.flush()
    return redirect('/')

def update(request):
        if request.method == 'POST' :
            x= Users.objects.get(id=request.session['id'])
            x.first_name = request.POST['first_name']
            x.last_name = request.POST['last_name']
            x.email = request.POST['email']
            x.password = request.POST['password']
            # updated_user = Users.objects.update(first_name=first_name, last_name=last_name, email=email,password=password)
            x.save()
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

