from django import forms
from django.core.exceptions import ValidationError

class ProfileForm(forms.Form):
  email = forms.EmailField(label='e-mail', max_length=254)
  company = forms.CharField(label='Company Name', max_length=254, required=False)
  company_type = forms.CharField(label='Company Type', max_length=254, required=False)
  company_subtype = forms.CharField(label='Company Sub Type', max_length=254, required=False)

  password = forms.CharField(widget=forms.PasswordInput(), label='Password (leave it blank if you do not want to change it)', max_length=254, required=False)
  repassword = forms.CharField(widget=forms.PasswordInput(), label='Re-enter password', max_length=254, required=False)
    
  def has_password(self):
    password = self.cleaned_data.get('password')
    if password:
      return True
    else:
      return False
    
  def clean_repassword(self):
    first_password = self.cleaned_data.get('password')
    second_password = self.cleaned_data.get('repassword')
    if first_password:
      if first_password != second_password:
        raise ValidationError('Passwords do not match')
