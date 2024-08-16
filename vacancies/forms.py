from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['Status']  # Exclude any fields you don't want to include in the form
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            # 'priority': forms.Select(attrs={'class': 'form-control'}),
            'vacancies': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills'}),
            'job_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'job_description':forms.Textarea(attrs={'class': 'form-control','placeholder': 'description'})
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application 
        exclude = ['job','created_date']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'CGPA'}),
            'year_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth Date', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class':'form-control', 'placeholder': 'Document'})
        }