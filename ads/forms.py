from django import forms
from .models import Ad, Comment
from django.core.files.uploadedfile import InMemoryUploadedFile
from .humanize import naturalsize

class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit) # STRING

    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'


    class Meta:
        model = Ad
        fields = ['title', 'text', 'tags' ,'price', 'picture']

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None: return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")
        
    
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance
    
class CommentForm(forms.ModelForm):
    text = forms.CharField(required=True, max_length=500, min_length=3, strip=True, label='Comment here')

    class Meta:
        model = Comment
        fields = ['text']