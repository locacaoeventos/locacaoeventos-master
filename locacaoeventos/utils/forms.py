from django import forms

from locacaoeventos.apps.place.placecore.models import PhotoProvisory

class TOCForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['autocomplete'] = "none-google"

class PhotoProvisoryForm(forms.ModelForm):
    class Meta:
        model = PhotoProvisory
        fields = ('photo', )