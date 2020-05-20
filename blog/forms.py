from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from blog.models import Photo


class PhotoCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name', 'url', 'description')
        widgets = {'url': forms.HiddenInput, }

        def clean_url(self):
            url = self.cleaned_data['url']
            valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('_', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions')
            return url

        def save(self, force_insert=False, force_update=False, commit=True):
            photo = super(PhotoCreateForm, self).save(commit=False)
            photo_url = self.cleaned_data['url']
            photo_name = '{}.{}'.format(slugify(photo.name), photo_url.rsplit('.', 1)[1].lower())
            response = request.urlopen(photo_url)
            photo.photo.save(photo_name, ContentFile(response.read()),save=False)
