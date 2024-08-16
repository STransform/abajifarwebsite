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
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255,default="Simon")
    lastname = models.CharField(max_length=255,default="Temesgen")
    email = models.EmailField(default="stemesgent@gmail.com")
    phone_number = models.CharField(max_length=15,default="0917436690")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2,default="3.16")
    year_of_experience = models.IntegerField(default=6)
    birth_date = models.DateTimeField(default=date(2000, 8, 14))
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    
    cv = models.FileField(upload_to='cv_files/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application from '{self.firstname} {self.lastname}' for: {self.job}"

    @staticmethod
    def get_list_fields():
        return ['firstname', 'lastname', 'phone_number', 'cgpa', 'year_of_experience', 'birth_date', 'gender', 'email', 'cv', 'created_date']

    list_fields = get_list_fields()