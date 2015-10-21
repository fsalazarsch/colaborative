from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class ProjectForm(forms.Form):
  project_name = forms.CharField(label='Project Name', max_length=255, required=False)
