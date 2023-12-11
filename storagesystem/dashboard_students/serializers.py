from rest_framework import serializers
#from dashboard_students.models import LNMOnline
from mpesa.models import LNMOnline


class LNMOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMOnline
        fields = ("id",)