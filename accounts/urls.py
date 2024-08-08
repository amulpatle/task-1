from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('registerUser/',views.registerUser,name="registerUser"),
    path('registerPatient/',views.registerPatient,name="registerPatient"),
     
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('DoctorDashboard/',views.DoctorDashboard,name='DoctorDashboard'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('PatientDashboard/',views.PatientDashboard,name="PatientDashboard"),
    path('post/<int:id>/', views.blog_post_detail, name='blog_post_detail'),
    path('my_blog_post_detail/<int:id>/',views.my_blog_post_detail,name="my_blog_post_detail"),
    
    path('doctor_list/',views.doctor_list,name='doctor_list'),
    path('book_appointment/<int:id>/',views.book_appointment,name='book_appointment'),
    path('appointment_detail/<int:id>/',views.appointment_detail,name='appointment_detail'),
     
]