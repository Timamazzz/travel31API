from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications_app.views import ApplicantViewSet, MunicipalityViewSet, SchoolViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'applicants/', ApplicantViewSet)
router.register(r'municipalities/', MunicipalityViewSet)
router.register(r'schools/', SchoolViewSet)
router.register(r'applications/', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
