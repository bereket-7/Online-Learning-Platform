from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    field = forms.CharField(max_length=50)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "field", "photo", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.profile.phone = self.cleaned_data["phone"]
        user.profile.field = self.cleaned_data["field"]
        user.profile.photo = self.cleaned_data["photo"]
        
        if commit:
            user.save()
        return user
