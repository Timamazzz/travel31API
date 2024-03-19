from applications_app.filters import ApplicantFilter, ApplicationFilter, SchoolFilter
from applications_app.models import Applicant, Municipality, School, Application
from applications_app.serailizers.applicant_serializers import ApplicantSerializer
from applications_app.serailizers.application_serializers import ApplicationSerializer
from applications_app.serailizers.municipality_serializers import MunicipalitySerializer
from applications_app.serailizers.school_serializers import SchoolSerializer
from travel31API.utils.ModelViewSet import ModelViewSet


# Create your views here.
class ApplicantViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    filterset_class = ApplicantFilter


class MunicipalityViewSet(ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilter
