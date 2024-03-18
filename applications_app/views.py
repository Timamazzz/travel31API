from applications_app.filters import ApplicantFilter
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
    serializer_list = {
        'retrieve': ApplicantSerializer,
        'create': ApplicantSerializer,
    }


class MunicipalityViewSet(ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    serializer_list = {
        'list': MunicipalitySerializer,
    }


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    serializer_list = {
        'list': SchoolSerializer,
    }


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    serializer_list = {
        'create': ApplicationSerializer,
    }
