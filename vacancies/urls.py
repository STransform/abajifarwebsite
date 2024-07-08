from django.urls import path
from .views import *  

urlpatterns = [
    path('job_list/', job_list, name='job_list'),
    path('job_apply/<int:pk>/', jobs_apply.as_view(), name = 'jobs_apply'),
]

