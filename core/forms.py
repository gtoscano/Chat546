from django import forms
from core.models import User
from django.core.exceptions import ValidationError


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full max-w-xs",
                "placeholder": "Username",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full max-w-xs",
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full max-w-xs",
                "placeholder": "Last Name",
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full max-w-xs",
                "placeholder": "Email Address",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_id = self.instance.id
        if User.objects.exclude(id=user_id).filter(username__iexact=username).exists():
            raise ValidationError(
                "This username is already taken. Please choose a different one."
            )
        return username
