from django import forms

class ImportForm(forms.Form):

    blog_slug = forms.CharField("Blog slug")
    input_file = forms.FileField()

    format = forms.CharField("Import format", widget=forms.HiddenInput, initial="WXR")