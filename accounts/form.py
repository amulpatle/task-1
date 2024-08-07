from django import forms
from .models import User
from .models import Doctor,Appointment

# from .validators import allow_only_images_validator
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','address','country','state','city','pin_code','password']
    
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
            

class EditDoctorProfile(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['profile_picture','speciality']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['speciality','date','start_time']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }     
   
