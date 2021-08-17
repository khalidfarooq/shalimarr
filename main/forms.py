from django.forms import ModelForm
from .models import *


class TrusteeForm(ModelForm):
    class Meta:
        model = Trustee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control","placeholder":"Enter username"})
        self.fields["email"].widget.attrs.update({"class": "form-control","placeholder":"Enter Email"})

