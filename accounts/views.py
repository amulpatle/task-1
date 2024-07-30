from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.utils import detectUser

from .models import User, UserProfile
from accounts.form import UserForm,UserProfileForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import  PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.contrib import auth
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'home.html')


def registerUser(request):
    
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid(): 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role =  User.DOCTOR
            user.save()
            return redirect('home')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        form_1 = UserProfileForm()
    
    context = {
            'form':form,
            'form_1':form_1,
        }
    return render(request,'registerUser.html',context)


def registerPatient(request):
    
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid(): 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role =  User.PATIENT
            user.save()
            return redirect('home')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        form_1 = UserProfileForm()
    
    context = {
            'form':form,
            'form_1':form_1,
        }
    return render(request,'registerPatient.html',context)


def login(request):
    if request.user.is_authenticated:
        print(request.user.role)
        if request.user.role==1 :
            return redirect('DoctorDashboard')
        elif request.user.role == 2:
            return redirect('PatientDashboard')
        return HttpResponse("already login")
    
    if request.method == 'POST':
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        
        user = auth.authenticate(request, email=email, password=password)
        print(user)
        print(user.role)
        if user is not None:
            auth.login(request, user)
            if request.user.role==1 :
                return redirect('DoctorDashboard')
            elif request.user.role == 2:
                return redirect('PatientDashboard')
            return HttpResponse("already login")
            
        else:
            error_message = 'Invalid email or password'
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')



@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

def DoctorDashboard(request):
    print(request.user.first_name)
    print(request.user.last_name)
    print(request.user.email)
    # print(request.user.state)
    
    context = {
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'email':request.user.email,
    }
    
    return render(request,'DoctorDashboard.html',context)

def PatientDashboard(request):
    context = {
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'email':request.user.email,
    }
    return render(request,'PatientDashboard.html',context)

def logout(request):
    auth.logout(request)
    
    return redirect('login')