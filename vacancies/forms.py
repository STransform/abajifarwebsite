# /home/simon/otech-website/vacancies/forms.py
from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['Status']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'vacancies': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills'}),
            'job_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }

class ApplicationForm(forms.Form):
    partner_name = forms.CharField(max_length=100, label="Full Name")
    email_from = forms.EmailField(label="Email")
    partner_phone = forms.CharField(max_length=20, required=False, label="Phone")
    cgpa_requirement = forms.FloatField(required=False, label="CGPA")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Birth Date")
    experience = forms.IntegerField(required=False, initial=0, label="Experience")
    linkedin_profile = forms.URLField(required=False, label="LinkedIn Profile")
    applicant_notes = forms.CharField(widget=forms.Textarea, required=False, label="Notes")
    cv = forms.FileField(required=False, label="Resume")