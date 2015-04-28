from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from countries.models import Country

class UserCreateForm(UserCreationForm):
    country = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "country")

    def save(self, commit=True):
        u = super(UserCreateForm, self).save(commit=False)
        u.email=self.cleaned_data["email"]
        if commit:
            u.save()
            c=Country(user=u, name=self.cleaned_data["country"])
            c.save()
        return u