import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otech_app.settings')
django.setup()

from dashboard.models import FAQ

faqs = FAQ.objects.all()
for faq in faqs:
    print(f"FAQ ID: {faq.id}, Q: {faq.question}, A: {faq.answer}")
    if "Otech" in faq.answer or "Otech" in faq.question or "OTech" in faq.answer or "OTech" in faq.question:
        faq.answer = faq.answer.replace("Otech", "Abajifar").replace("OTech", "Abajifar")
        faq.question = faq.question.replace("Otech", "Abajifar").replace("OTech", "Abajifar")
        faq.save()
        print(f"Updated FAQ {faq.id}")

from about_us.models import Service
print("SERVICES:", list(Service.objects.values_list('title', flat=True)))

from core.models import Settings
stg = Settings.objects.first()
if stg:
    print("SETTINGS:", stg.address, stg.email, stg.phone)
