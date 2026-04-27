from django.contrib import admin

from .models import Application, Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("job_title", "job_type", "cgpa_requirement", "Status", "location", "job_deadline")
    list_filter = ("Status", "job_type", "level")
    search_fields = ("job_title", "job_description", "location", "skills")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("partner_name", "email_from", "partner_phone", "cgpa_requirement", "job_odoo_id", "experience", "created_at")
    list_filter = ("created_at", "cgpa_requirement", "experience")
    search_fields = ("partner_name", "email_from", "partner_phone", "linkedin_profile")
