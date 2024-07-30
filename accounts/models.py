from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.fields.related import OneToOneField,ForeignKey


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
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    DOCTOR = 1
    PATIENT = 2
    
    ROLE_CHOICE = (
        (DOCTOR,'Doctor'),
        (PATIENT,'Patient'),
    )
    
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
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
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    
   
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Doctor'
        elif self.role ==2:
            use_role = 'Patient'
        return user_role
    

    
    
    
    