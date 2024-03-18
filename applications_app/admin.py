from django.contrib import admin
from .models import Municipality, School, Applicant, Application


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'municipality']


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'phone_number']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'full_name', 'school', 'child_full_name', 'child_gender', 'child_age',
                    'received_offer', 'duration']
