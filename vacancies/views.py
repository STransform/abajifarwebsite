from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from .forms import ApplicationForm
from .odoo_utils import fetch_odoo_jobs, create_odoo_application
from django.core.mail import EmailMultiAlternatives
import mimetypes
import base64
from datetime import datetime, timedelta
from django.db.models import Q
from .models import Application, Job

def job_list(request):
    search = request.GET.get('search', None)
    page_number = request.GET.get('page', 1)
    
    # Fetch jobs from Odoo
    jobs = fetch_odoo_jobs(search)
    
    # Fallback to local Job model if no Odoo jobs
    if not jobs:
        messages.warning(request, "No jobs found in Odoo. Displaying local jobs. Check Odoo configuration and server console for details.")
        jobs = Job.objects.filter(Status='Active')
        if search:
            jobs = jobs.filter(Q(job_title__icontains=search) | Q(job_description__icontains=search))
        jobs = jobs.values('id', 'job_title', 'job_description', 'job_deadline', 'location', 'level')
        for job in jobs:
            job['name'] = job['job_title']
            job['job_description'] = job.get('job_description', '')
            job['career_level'] = job.get('level', 'Not Specified')
            job['cgpa_requirement'] = 0.0  # Local model doesn't have CGPA, default to 0.0
            job['date_to'] = job['job_deadline']
            job['address_id'] = False
    
    # Process job data for template
    for job in jobs:
        job['job_title'] = job['name']
        job['job_description'] = job.get('job_description', '')
        job['job_deadline'] = job.get('date_to', '')
        job['location'] = job['address_id'][1] if job.get('address_id') and isinstance(job['address_id'], (list, tuple)) else job.get('location', 'Remote')
        job['Status'] = job.get('Status', 'Active' if job.get('is_published', True) else 'Closed')
        job['career_level'] = job.get('career_level', 'Not Specified')
        job['cgpa_requirement'] = job.get('cgpa_requirement', 0.0)

    # Paginate jobs
    paginator = Paginator(jobs, 12)
    page_obj = paginator.get_page(page_number)

    return render(request, 'front/vacancy.html', {
        'jobs': page_obj.object_list,
        'page_obj': page_obj,
        'search': search
    })

class jobs_apply(View):
    def get(self, *args, **kwargs):
        job_id = self.kwargs['pk']
        jobs = fetch_odoo_jobs()
        # Try local Job model if Odoo job not found
        job = next((j for j in jobs if j['id'] == job_id), None)
        if not job:
            try:
                local_job = Job.objects.get(id=job_id, Status='Active')
                job = {
                    'id': local_job.id,
                    'name': local_job.job_title,
                    'job_title': local_job.job_title,
                    'job_description': local_job.job_description,
                    'date_to': local_job.job_deadline,
                    'location': local_job.location,
                    'Status': local_job.Status,
                    'career_level': local_job.level,
                    'cgpa_requirement': 0.0,
                    'address_id': False,
                    'company_id': False,
                    'department_id': False,
                }
            except Job.DoesNotExist:
                messages.error(self.request, "Job not found.")
                return redirect('job_list')
        form = ApplicationForm()
        return render(self.request, 'front/vacancy_apply.html', {'form': form, 'job': job})

    def post(self, *args, **kwargs):
        form = ApplicationForm(self.request.POST, self.request.FILES)
        job_id = self.kwargs['pk']
        if form.is_valid():
            jobs = fetch_odoo_jobs()
            job = next((j for j in jobs if j['id'] == job_id), None)
            is_local_job = False
            if not job:
                try:
                    local_job = Job.objects.get(id=job_id, Status='Active')
                    job = {
                        'id': local_job.id,
                        'name': local_job.job_title,
                        'job_description': local_job.job_description,
                        'date_to': local_job.job_deadline,
                        'company_id': False,
                        'department_id': False,
                    }
                    is_local_job = True
                except Job.DoesNotExist:
                    messages.error(self.request, "Job not found.")
                    return render(self.request, 'front/vacancy_apply.html', {'form': form})

            # Prepare application data for Odoo
            vals = {
                'partner_name': form.cleaned_data['partner_name'],
                'email_from': form.cleaned_data['email_from'],
                'partner_phone': form.cleaned_data['partner_phone'],
                'cgpa_requirement': form.cleaned_data['cgpa_requirement'] or 0.0,
                'job_id': job_id,
                'linkedin_profile': form.cleaned_data.get('linkedin_profile', ''),
                'experience': form.cleaned_data['experience'] or 0.0,
                'applicant_notes': form.cleaned_data.get('applicant_notes', ''),
                'company_id': job['company_id'][0] if job.get('company_id') and isinstance(job['company_id'], (list, tuple)) else False,
                'department_id': job['department_id'][0] if job.get('department_id') and isinstance(job['department_id'], (list, tuple)) else False,
            }

            # Handle CV file
            if form.cleaned_data['cv']:
                cv_file = form.cleaned_data['cv']
                vals['cv_filename'] = cv_file.name
                vals['cv_data'] = base64.b64encode(cv_file.read()).decode('utf-8')

            # Create application in Odoo (unless local job)
            try:
                if not is_local_job:
                    applicant_id = create_odoo_application(vals)
                else:
                    applicant_id = None
                # Save to local Application model
                Application.objects.create(
                    firstname=vals['partner_name'],
                    email=vals['email_from'],
                    phone=vals['partner_phone'],
                    cgpa=vals['cgpa_requirement'],
                    birth_date=form.cleaned_data.get('birth_date'),
                    year_of_experience=vals['experience'],
                    linkedin_profile=vals['linkedin_profile'],
                    applicant_notes=vals['applicant_notes'],
                    job_odoo_id=job_id,
                    cv=form.cleaned_data['cv'] if form.cleaned_data['cv'] else None
                )

                # Send email notification
                msg = f"An applicant named {vals['partner_name']} has submitted an application for the job: {job['name']}"
                email = "stemesgent@gmail.com"
                e = EmailMultiAlternatives(
                    subject=f"New Job Application from: {vals['partner_name']}",
                    body=msg,
                    from_email="OTECH",
                    to=[email]
                )
                if form.cleaned_data['cv']:
                    cv_file.seek(0)
                    mime_type, _ = mimetypes.guess_type(cv_file.name)
                    e.attach(cv_file.name, cv_file.read(), mime_type)
                e.send()

                messages.success(self.request, "Applied Successfully.")
                return redirect('job_list')
            except Exception as e:
                print(f"Application submission error: {str(e)}")
                messages.error(self.request, f"Error submitting application: {str(e)}")
                return render(self.request, 'front/vacancy_apply.html', {'form': form})

        messages.error(self.request, "Invalid Data")
        return render(self.request, 'front/vacancy_apply.html', {'form': form})

def application_list(request):
    search = request.GET.get('search', None)
    min_cgpa = request.GET.get('min_cgpa', None)
    min_age = request.GET.get('min_age', None)
    min_experience = request.GET.get('min_experience', None)

    filters = Q()
    if search:
        filters &= (Q(firstname__icontains=search) | Q(email__icontains=search))
    if min_cgpa:
        try:
            filters &= Q(cgpa__gte=float(min_cgpa))
        except ValueError:
            pass
    if min_age:
        try:
            min_birth_date = datetime.now() - timedelta(days=365 * int(min_age))
            filters &= Q(birth_date__lte=min_birth_date)
        except ValueError:
            pass
    if min_experience:
        try:
            filters &= Q(year_of_experience__gte=int(min_experience))
        except ValueError:
            pass

    applications = Application.objects.filter(filters)

    return render(request, 'front/applied_jobs_list.html', {
        'applications': applications,
        'search': search,
        'min_cgpa': min_cgpa,
        'min_age': min_age,
        'min_experience': min_experience
    })