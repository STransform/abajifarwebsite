from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Job
def add_vacancy(request):
    return render(request, 'job_post_add.html')
from django.shortcuts import render, redirect
from .forms import  ApplicationForm  # Assuming your form is in a file named forms.py
from .models import Job
from django.views import View
from django.core.mail import EmailMultiAlternatives

from core.views import paginate

def job_list(request):
    search = request.GET.get('search', None)
    if search:
        jobs = Job.objects.filter(Status = 'Active', job_title__icontains = search, 
                                  job_description__icontains=search, skills__icontains = search )
    else:
        jobs = Job.objects.filter(Status = 'Active')

    jobs_list = paginate( jobs, 5, request)

    return render(request, 'front/vacancy.html', {'jobs': jobs_list, 'search':search})
    
    
class jobs_apply(View):
    def get(self, *args, **kwargs):
        
        job = Job.objects.get(id = self.kwargs['pk'])
        form = ApplicationForm()
        return render(self.request, 'front/vacancy_apply.html', {'form':form, 'job':job} )
    
    def post(self, *args, **kwargs):
        form = ApplicationForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            ap = form.save(commit=False)
            ap.job =Job.objects.get(id = self.kwargs['pk'])
            ap.save()

            msg = f"An applicant named {ap.name} has submitted an application for the job: {ap.job} "
            email = "stemesgent@gmail.com"
            e = EmailMultiAlternatives(f"New Job Application from : {ap.name}",msg,from_email="OTECH",to=[str(email)], )
            m = e.send()
            
            messages.success(self.request, ("Applied Successfully."))
            return redirect('/vacancies/job_list/')
        
        messages.error(self.request, "Invalid Data")
        return render(self.request, 'front/vacancy_apply.html', {'form':form} )
    
