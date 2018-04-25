from django import forms
from .models import Author,Book,Genre,BookInstance
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
#email
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']

    def clean(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date-Date cannot be from the past.'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date-Enter a date between today and next 4 weeks'))

        return data

    def __init__(self, *args, **kwargs):
        super(BorrowBookForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'placeholder': 'YYYY-MM-DD'})

class RenewForm(forms.Form):
    renew_date = forms.DateField(help_text="Enter a date from today to next 3 weeks")

    def clean_renew_date(self):
        data = self.cleaned_data['renew_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date-Date cannot be from the past.'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date-Enter a date between today and next 4 weeks'))

        return data

class AddBooksForm(forms.ModelForm):
    title = forms.CharField(help_text="Enter the title", max_length=300)
    #authors_list = Author.objects.all()
    #authors = forms.ChoiceField(choices =[(x,x) for x in authors_list], help_text="Author")
    #genre_list = Genre.objects.all(*)
    #genres = forms.ChoiceField(choices=[(x, x) for x in genre_list], help_text="Enter the genre")
    summary = forms.CharField(help_text="Add a summary to the book", required=False, widget=forms.Textarea())
    ISBN = forms.IntegerField(help_text="13 digit ISBN number", required=False)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'genre', 'summary', 'ISBN']

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         summary = cleaned_data.get('summary')

#         if summary:
#             summary= 'xyz'
#             cleaned_data['summary']=summary

#         return cleaned_data

#Email
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
