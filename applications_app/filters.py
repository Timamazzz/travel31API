from django_filters import rest_framework as filters

from applications_app.models import Applicant, Application


class ApplicantFilter(filters.FilterSet):
    phone_number = filters.CharFilter(lookup_expr='icontains')
    telegram_id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Applicant
        fields = ['phone_number', 'telegram_id']


class ApplicationFilter(filters.FilterSet):
    telegram_id = filters.CharFilter(field_name="applicant__telegram_id")

    class Meta:
        model = Application
        fields = ['telegram_id', ]
