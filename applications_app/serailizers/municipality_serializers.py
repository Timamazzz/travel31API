from rest_framework import serializers
from applications_app.models import Municipality
from applications_app.serailizers.school_serializers import SchoolSerializer


class MunicipalitySerializer(serializers.ModelSerializer):
    schools = SchoolSerializer(many=True, read_only=True)

    class Meta:
        model = Municipality
        fields = '__all__'
