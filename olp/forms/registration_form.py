from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from olp.models import Role, Profile
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
        
        if commit:
            user.save()
            
            # Create profile and save additional fields
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                field=self.cleaned_data["field"],
                photo=self.cleaned_data["photo"],
            )
            
        return user

