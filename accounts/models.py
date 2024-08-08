from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db.models.fields.related import OneToOneField,ForeignKey
from datetime import date, datetime, timedelta

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,phone_number=None,password=None,address=None, country=None, state=None, city=None, pin_code=None):
        if not email:
            raise ValueError('User must  have an email address')
        
        if not username:
            raise ValueError('User  must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number=phone_number,
            address=address,
            country=country,
            state=state,
            city=city,
            pin_code=pin_code,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,   
        )
        user.is_admin = True
        user.is_active =  True
        user.is_staff = True
        user.is_superadmin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    DOCTOR = 1
    PATIENT = 2
    
    ROLE_CHOICE = (
        (DOCTOR,'Doctor'),
        (PATIENT,'Patient'),
    )
    
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    # profile_picture = models.ImageField(upload_to='Doctor_profile/', blank=True, null=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=12,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
    address = models.CharField(max_length=250,blank=True,null=True)
    
    country = models.CharField(max_length=15,blank=True,null=True)
    state = models.CharField(max_length=15,blank=True,null=True)
    city = models.CharField(max_length=15,blank=True,null=True)
    pin_code = models.CharField(max_length=6,blank=True,null=True)
    # Requierd fields
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Custom related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        
        return f"{self.first_name} {self.last_name}"
   
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Doctor'
        elif self.role ==2:
            use_role = 'Patient'
        return user_role
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class Doctor(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='Doctor_profile/', blank=True, null=True)
    speciality = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    
    
class Appointment(models.Model):
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointments')
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments')
    speciality = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def end_time(self):
        return (datetime.combine(date.min, self.start_time) + timedelta(minutes=45)).time()

    
    def __str__(self):
        return f"{self.patient.username} with {self.doctor.user.username} on {self.date} at {self.start_time}"