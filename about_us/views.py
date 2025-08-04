from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.db.models.base import ModelBase

 
def about(request): # Render about us page 
    about_data = About.objects.first()
    team_members = TeamMember.objects.all()
    context = {
        'about_data': about_data,
        'team_members': team_members,
    }

    return render(request, 'front/about.html', context)


def bureau_structure(request): # Render structure page 
    structure_data = BureauStructure.objects.first()
    return render(request, 'front/structure.html', {'structure_data': structure_data})


class ServicesPage(View): # Render service page 
    def get(self, request, **kwargs):
        services = Service.objects.all()
        return render(request, "front/services.html", {'services':services})


class TechnologyPage(View): # Render technology page 
    def get(self, request, **kwargs):
        technology = Technology.objects.all()
        return render(request, "front/technology.html", {'technology':technology})

class InfrastructurePage(View): # Render infrastructure page 
    def get(self, request, **kwargs):
        infrastructure = Infrastructure.objects.all()
        return render(request, "front/infrastructure.html", {'infrastructure':infrastructure})

class InnovationPage(View): # Render innovation page 
    def get(self, request, **kwargs):
        innovation = Innovation.objects.all()
        return render(request, "front/innovation.html", {'innovation':innovation})
    
class CompanyValuesPage(View): # Render values page 
    def get(self, request, **kwargs):
        values = CompanyValues.objects.all()
        return render(request, "front/company_values.html", {'values':values})
class VisionMissionPage(View): # Render service page 
    def get(self, request, **kwargs):
        vision_mission = VisionMission.objects.all()
        return render(request, "front/vision_mission.html", {'vision_mission':vision_mission})

class VisionPage(View): # Render service page 
    def get(self, request, **kwargs):
        vision = Vision.objects.all()
        return render(request, "front/vision.html", {'vision':vision})
class OtechExcellencePage(View): # Render service page 
    def get(self, request, **kwargs):
        otech_excellence = OtechExcellence.objects.all()
        return render(request, "front/otech_excellence.html", {'otech_excellence':otech_excellence})
class WhatPeopleSaysPage(View): # Render service page 
    def get(self, request, **kwargs):
        people_saying = WhatPeopleSays.objects.all()
        return render(request, "front/people_saying.html", {'people_saying':people_saying})
class AboutOtechFooterPage(View): # Render service page 
    def get(self, request, **kwargs):
        about_footer = AboutOtechFooter.objects.all()
        return render(request, "front/about_footer.html", {'about_footer':about_footer})
    
class ElevatingSkillsPage(View): # Render service page 
    def get(self, request, **kwargs):
        elevating_skills = ElevatingSkills.objects.all()
        return render(request, "front/elevating_skills.html", {'elevating_skills':elevating_skills})

class OurPartnersPage(View): # Render service page 
    def get(self, request, **kwargs):
        our_partners = OurPartners.objects.all()
        return render(request, "front/our_partners.html", {'our_partners':our_partners})
