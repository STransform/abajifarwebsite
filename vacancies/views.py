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
import mimetypes
from django.core.files.storage import default_storage
from core.views import paginate
from .models import Application
from django.db.models import Q
from datetime import datetime, timedelta

class AppliedJobsListView(View):
    model = Application
    template_name = 'front/applied_jobs_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.select_related('job').all()
    
def application_list(request):
    search = request.GET.get('search', None)
    min_cgpa = request.GET.get('min_cgpa', None)
    min_age = request.GET.get('min_age', None)
    min_experience = request.GET.get('min_experience', None)  # Add this line

    # Calculate the minimum birthdate based on the required age
    if min_age:
        try:
            min_birth_date = datetime.now() - timedelta(days=365 * int(min_age))
        except ValueError:
            min_birth_date = datetime(2024, 1, 1)  # Default to a very old date if there's a value error
    else:
        min_birth_date = datetime(2024, 1, 1)  # No filter on age
    
    # Build the query filters dynamically
    filters = Q()
    if search:
        filters &= (Q(firstname__icontains=search) |
                    Q(email__icontains=search) |
                    Q(job__job_title__icontains=search))
    if min_cgpa:
        try:
            filters &= Q(cgpa__gte=float(min_cgpa))
        except ValueError:
            pass  # Ignore invalid CGPA values
    filters &= Q(birth_date__lte=min_birth_date)
    if min_experience:
        try:
            filters &= Q(year_of_experience__gte=int(min_experience))
        except ValueError:
            pass  # Ignore invalid experience values
    
    # Apply filters
    applications = Application.objects.filter(filters)
    
    return render(request, 'front/applied_jobs_list.html', {
        'applications': applications,
        'search': search,
        'min_cgpa': min_cgpa,
        'min_age': min_age,
        'min_experience': min_experience  
    })

def job_list(request):
    search = request.GET.get('search', None)
    if search:
        jobs = Job.objects.filter(
            Status='Active',
            job_title__icontains=search,
            job_description__icontains=search,
            skills__icontains=search
        )
    else:
        jobs = Job.objects.filter(Status='Active')

    return render(request, 'front/vacancy.html', {'jobs': jobs, 'search': search})

class jobs_apply(View):
    def get(self, *args, **kwargs):
        job = Job.objects.get(id=self.kwargs['pk'])
        form = ApplicationForm()
        return render(self.request, 'front/vacancy_apply.html', {'form': form, 'job': job})

    def post(self, *args, **kwargs):
        form = ApplicationForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            ap = form.save(commit=False)
            ap.job = Job.objects.get(id=self.kwargs['pk'])
            ap.save()

            # Prepare the email
            msg = f"An applicant named {ap.firstname} has submitted an application for the job: {ap.job}"
            email = "stemesgent@gmail.com"
            e = EmailMultiAlternatives(
                subject=f"New Job Application from: {ap.firstname}",
                body=msg,
                from_email="OTECH",
                to=[email]
            )

            # Attach the CV file
            if ap.cv:
                # Get the path of the file
                cv_path = ap.cv.path

                # Guess the mimetype of the file
                mime_type, _ = mimetypes.guess_type(cv_path)

                # Read the file content and attach it to the email
                with default_storage.open(cv_path, 'rb') as cv_file:
                    e.attach(ap.cv.name, cv_file.read(), mime_type)

            # Send the email
            e.send()

            messages.success(self.request, "Applied Successfully.")
            return redirect('/vacancies/job_list/')
        
        messages.error(self.request, "Invalid Data")
        return render(self.request, 'front/vacancy_apply.html', {'form': form})