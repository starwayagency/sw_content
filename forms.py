from django import forms 
from .models import Page, Text, Img



# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_changelist_form


class PageAdminForm(forms.ModelForm):
    meta_title = forms.CharField(max_length=255)
    meta_descr = forms.Textarea(attrs={'cols': '10', 'rows': '5'})
    meta_key   = forms.Textarea(attrs={'cols': '30', 'rows': '5'})
    class Meta:
        model = Page 
        fields = [
            'code',
            'meta_title',
            'meta_descr',
            'meta_key',
        ]

