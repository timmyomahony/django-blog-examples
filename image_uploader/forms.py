from .utils import *

from django.utils.translation import ugettext as _
from django import forms


class UploadURLForm(forms.Form):
    url = forms.URLField(required=True,
        error_messages={
            "required": "Please enter a valid URL to an image (.jpg .jpeg .png)"
        },
    )

    def clean_url(self):
        url = self.cleaned_data['url'].lower()
        domain, path = split_url(url)
        if not valid_url_extension(url) or not valid_url_mimetype(url):
            raise forms.ValidationError(_("Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)"))
        return url