from django import forms
from .models import Author, Quote
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname','born_date','born_location','description']
class QuoteForm(forms.ModelForm):
    tags_text = forms.CharField(label='Теги (через кому)', required=False)
    class Meta:
        model = Quote
        fields = ['quote','author']
    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tags = [t.strip().lower() for t in self.cleaned_data['tags_text'].split(',') if t.strip()]
        if commit: obj.save()
        return obj
