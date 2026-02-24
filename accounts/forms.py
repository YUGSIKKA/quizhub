from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Register as:",
        required=True
    )
    phone = forms.CharField(max_length=15, required=False, label="Phone Number")
    institution = forms.CharField(max_length=200, required=False, label="School/College/Institution")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create associated profile
            profile = Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data.get('phone', ''),
                institution=self.cleaned_data.get('institution', '')
            )
        return user


class SettingsForm(forms.ModelForm):
    """Allow users to update their username, email and preferred language."""
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ]

    preferred_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']
