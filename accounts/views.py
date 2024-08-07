from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.utils import detectUser

from .models import User
from accounts.form import UserForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import  PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.contrib import auth
from django.http import HttpResponse
from BlogPost.forms import BlogPostForm

from BlogPost.models import BlogPost
from accounts.models import User
from django.shortcuts import get_object_or_404
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
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            pin_code = form.cleaned_data['pin_code']
            
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,email=email,address=address,country=country,state=state,city=city,pin_code=pin_code,password=password)
            user.role =  User.DOCTOR
            user.save()
            return redirect('home')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        
    
    context = {
            'form':form,
           
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
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            pin_code = form.cleaned_data['pin_code']
            
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,email=email,address=address,country=country,state=state,city=city,pin_code=pin_code,password=password)
            user.role =  User.PATIENT
            user.save()
            return redirect('home')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        
    
    context = {
            'form':form,
            
        }
    return render(request,'registerPatient.html',context)


def login(request):
    if request.user.is_authenticated:
        print(request.user)
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
        'phone_number':request.user.phone_number,
        'city':request.user.city,
        'state':request.user.state,
        'country':request.user.country,
        'pin_code':request.user.pin_code,
    }
    
    return render(request,'DoctorDashboard.html',context)

def edit_profile(request):
    return render(request,'doctor/edit_profile.html')

def PatientDashboard(request):
    
    all_post = BlogPost.objects.all()
    doctors = User.objects.filter(role=User.DOCTOR)
    print(doctors[0].username)
    
    context = {
        'all_post':all_post,
    }
    return render(request,'PatientDashboard.html',context)

def logout(request):
    auth.logout(request)
    
    return redirect('home')

def blog_post_detail(request,id):
    post = get_object_or_404(BlogPost,id=id)
    context = {
        'post':post,
    }
    return render(request,'blog_post_detail.html',context)

def my_blog_post_detail(request,id):
    post = get_object_or_404(BlogPost,id=id)
    context = {
        'post':post,
    }
    return render(request,'my_blog_posts_details.html',context)


def doctor_list(request):
    doctors = User.objects.filter(role=User.DOCTOR)  # Ensure 'role' field and 'User.DOCTOR' constant are defined
    context = {
        'doctors': doctors
    }
    return render(request, 'doctor_list.html', context)


def book_appointment(request,id):
    print(request,id)
    doctor = User.objects.filter(id=id)
    print(doctor[0].username)
    return HttpResponse('success')

