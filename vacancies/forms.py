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
            'name':forms.TextInput(attrs={'class':'form-control', 'label':'Full Name', 'placeholder': 'Full Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'label':'Email', 'placeholder': 'Email'}),
            'cv':forms.FileInput(attrs={'class':'form-control', 'label':'Cover Letter Document', 'placeholder': 'Document'})
        }