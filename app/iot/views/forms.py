from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('alive_monitoring', 'send_message_to_email', 'line_token', 'send_message_to_line')