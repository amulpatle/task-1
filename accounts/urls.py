from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
     path('registerUser/',views.registerUser,name="registerUser"),
     path('registerPatient/',views.registerPatient,name="registerPatient"),
     
     path('login/',views.login,name='login'),
     path('logout/',views.logout,name='logout'),
     path('DoctorDashboard/',views.DoctorDashboard,name='DoctorDashboard'),
     path('PatientDashboard/',views.PatientDashboard,name="PatientDashboard")
]