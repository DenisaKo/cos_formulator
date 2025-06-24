from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    """
    Include an email field
    and custom validation for email uniqueness.
    """
    # Define the email field as required.
    email = forms.EmailField(
        required=True,
        label="Email Address",
        help_text="Your email address will be used for account recovery."
    )

    class Meta(UserCreationForm.Meta): 
        model = User
        fields = ["username", "email"] #email is added
        
    # Custom clean method for form-wide validation, especially for email uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                "This email address is already registered. Please use a different one or log in.",
                code='email_taken'
            )
        return email