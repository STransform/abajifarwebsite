from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from core.views import paginate

from .forms import ApplicationForm
from .models import Application, Job


def job_list(request):
    search = request.GET.get('search', "")
    jobs = Job.objects.filter(Status='Active').order_by('-id')

    if search:
        jobs = jobs.filter(
            Q(job_title__icontains=search)
            | Q(job_description__icontains=search)
            | Q(location__icontains=search)
            | Q(skills__icontains=search)
        )

    jobs_list = paginate(jobs, 12, request)

    return render(request, 'front/vacancy.html', {
        'jobs': jobs_list,
        'page_obj': jobs_list,
        'search': search,
        'page_title': 'Vacancies',
        'page_subtitle': 'Explore Our Current Job Openings',
        'announcement_page': True
    })


class jobs_apply(View):
    def _get_job(self, job_id):
        return get_object_or_404(Job, id=job_id, Status='Active')

    def _render_page(self, job, form):
        return render(
            self.request,
            'front/vacancy_apply.html',
            {
                'form': form,
                'job': job,
                'page_title': 'Apply for Vacancy',
                'page_subtitle': 'Fill in the details to apply for the vacancy',
                'announcement_page': True,
            }
        )

    def get(self, request, *args, **kwargs):
        job = self._get_job(self.kwargs['pk'])
        return self._render_page(job, ApplicationForm(job=job))

    def post(self, *args, **kwargs):
        job = self._get_job(self.kwargs['pk'])
        form = ApplicationForm(self.request.POST, self.request.FILES, job=job)

        if not form.is_valid():
            messages.error(self.request, "Please correct the highlighted fields and try again.")
            return self._render_page(job, form)

        Application.objects.create(
            partner_name=form.cleaned_data['partner_name'],
            email_from=form.cleaned_data['email_from'],
            partner_phone=form.cleaned_data.get('partner_phone') or '',
            cgpa_requirement=form.cleaned_data.get('cgpa_requirement'),
            experience=form.cleaned_data.get('experience') or 0,
            attachment_ids=form.cleaned_data.get('attachment_ids'),
            linkedin_profile=form.cleaned_data.get('linkedin_profile') or '',
            job_odoo_id=job.id,
        )

        messages.success(
            self.request,
            f"Your application for {job.job_title} was submitted successfully."
        )
        return redirect('jobs_apply', pk=job.id)


def application_list(request):
    if request.user.is_authenticated and request.user.has_perm('vacancies.view_application'):
        return redirect('list_view', model_name='Application')

    search = request.GET.get('search', None)
    min_cgpa = request.GET.get('min_cgpa', None)
    min_experience = request.GET.get('min_experience')

    filters = Q()
    if search:
        filters &= (Q(partner_name__icontains=search) | Q(email_from__icontains=search))
    if min_cgpa:
        try:
            filters &= Q(cgpa_requirement__gte=float(min_cgpa))
        except ValueError:
            pass
    if min_experience:
        try:
            filters &= Q(experience__gte=int(min_experience))
        except ValueError:
            pass

    applications = Application.objects.filter(filters)
    return render(request, 'front/applied_jobs_list.html', {
        'applications': applications,
        'search': search,
        'min_cgpa': min_cgpa,
        'min_experience': min_experience
    })
