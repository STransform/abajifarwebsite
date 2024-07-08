from django.db import models
from django.utils.translation import gettext as _

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
    job = models.ForeignKey(Job, on_delete = models.CASCADE,)
    name = models.CharField(max_length = 255, )
    email = models.EmailField()
    cv = models.FileField(blank=False)
    created_date = models.DateTimeField(auto_now_add =True)

    def __str__(self) -> str:
        return f"Application from '{self.name}' for : {self.job}"


    def get_list_fields():
        return ['name', 'email', 'cv', 'created_date']
    
    list_fields = get_list_fields()