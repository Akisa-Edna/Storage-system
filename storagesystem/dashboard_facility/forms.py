from django import forms
from dashboard_students.models import Container

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = '__all__'  # You can specify specific fields if needed


