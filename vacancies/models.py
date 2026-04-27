from django.db import models
from django.utils.html import format_html
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
    cgpa_requirement = models.FloatField(blank=True, null=True, help_text="Minimum CGPA required for this vacancy.")
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

    @property
    def name(self):
        return self.job_title

    @property
    def date_to(self):
        return self.job_deadline

    @property
    def career_level(self):
        return self.level

    def get_list_fields():
        return ['job_title', 'job_type', 'cgpa_requirement', 'Status', 'job_deadline']
    
    list_fields = get_list_fields()


class Application(models.Model):
    partner_name = models.CharField(max_length=100)
    email_from = models.EmailField()
    partner_phone = models.CharField(max_length=20, blank=True, null=True)  # Renamed from phone
    cgpa_requirement = models.FloatField(blank=True, null=True)
    experience = models.IntegerField(default=0)
    attachment_ids = models.FileField(upload_to='cvs/', blank=True, null=True)
    linkedin_profile = models.CharField(max_length=255, blank=True)
    # applicant_notes = models.TextField(blank=True, null=True)
    job_odoo_id = models.IntegerField()  # Store Odoo hr.job ID
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',) 

    def __str__(self):
        return f"{self.partner_name} - {self.job_odoo_id}"

    def get_job_title(self):
        job = Job.objects.filter(id=self.job_odoo_id).first()
        return job.job_title if job else f"Job #{self.job_odoo_id}"

    @property
    def applicant_cgpa(self):
        return self.cgpa_requirement

    def resume_link(self):
        if self.attachment_ids:
            return format_html(
                '<a href="{}" download>Download resume</a>',
                self.attachment_ids.url,
            )
        return "No resume"

    def get_list_fields():
        return ['partner_name', 'email_from', 'partner_phone', 'get_job_title', 'applicant_cgpa', 'experience', 'resume_link', 'created_at']

    list_fields = get_list_fields()
