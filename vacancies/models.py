from django.db import models
from django.utils.translation import gettext as _
from datetime import date
class Job(models.Model):
    job_title = models.CharField(max_length=255,help_text="Make sure to submit a max of 255 characters.")
    job_type = models.CharField(max_length=50, choices=[
        ('Contract', _('Contract')),
        ('Freelance', _('Freelance')),
        ('Full Time', _('Full Time')),
        ('Part Time', _('Part Time')),
        ('Internship', _('Internship')),
    ])
    vacancies = models.IntegerField(help_text="Number of open places.")
    job_description = models.TextField(null=True, blank=True)
    
    Status = models.CharField(max_length=50, choices=[
        ('Active', _('Active')),
        ('CLosed', _('CLosed')),
    ])

    skills = models.CharField(max_length=255,help_text="Make sure to submit a max of 255 characters.")
    job_deadline = models.DateField()
    location = models.CharField(max_length=255, default='',help_text="Make sure to submit a max of 255 characters.")  # Assuming location is a character field

    level = models.CharField(max_length=255, choices=[
        ('Junior', _('Junior')),
        ('Mid-Level', _('Mid-Level')),  
        ('Senior', _('Senior')),  
        ('Expert', _('Expert')),
    ])
    
    class Meta:
        ordering = ("-id",)
    
    def __str__(self):
        return self.job_title

    def get_list_fields():
        return ['job_title', 'job_type', 'Status', 'job_deadline']
    
    list_fields = get_list_fields()


class Application(models.Model):
    firstname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    year_of_experience = models.IntegerField(default=0)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    # linkedin_profile = models.URLField(blank=True, null=True)
    applicant_notes = models.TextField(blank=True, null=True)
    job_odoo_id = models.IntegerField()  # Store Odoo hr.job ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstname} - {self.job_odoo_id}"