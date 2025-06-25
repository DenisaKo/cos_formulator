from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Formulation, FormulationIngredient, Ingredient

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
    
class FormulationForm(forms.ModelForm):
    """
    Form for creating and updating a formulation.
    """
    class Meta: 
        model = Formulation
        fields = ["name", "description", "batch_size_grams"]

    widgets = {
        'name': forms.TextInput(attrs={'placeholder': 'e.g., Hydrating Face Cream'}),
        'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe your formulation (e.g., Intensive moisturising cream)'}),
        'instructions': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Step-by-step guide for making this formulation...'}),
        'batch_size_grams': forms.NumberInput(attrs={'placeholder': 'e.g., 100.00'})
    }
    labels = {
        'name': 'Formulation name',
        'description': 'Description',
        'instructions': 'Instructions',
        'batch_size_grams': 'Batch Size (grams)',
    } 
    help_texts = {
        'batch_size_grams': 'Enter the target batch size in grams (e.g., 100.00 for a 100g batch). Must be 0 or a positive number.',
    }

class IngredientForm(forms.ModelForm):
    """
    Form for creating and updating an ingredient.
    """
    class Meta: 
        model = Ingredient
        fields = ["name", "inci_name", "functionality", "solubility", "physical_state", "recommended_concentration", "notes"]

    widgets = {
        'name': forms.TextInput(attrs={'placeholder': 'e.g., Hydrating Face Cream'}),
        'inci_name': forms.TextInput(attrs={'placeholder': 'e.g., Sodium Chloride'}),
        'functionality': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe your formulation (e.g., Intensive moisturising cream)'}),
        'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Step-by-step guide for making this formulation...'}),
        'recommended_concentration': forms.TextInput(attrs={'placeholder': 'e.g., 5-10%'})
    }
    labels = {
        'name': 'Ingredient name',
        'inci_name': 'Ingredient INCI name',
        'functionality': 'Functionality',
        'notes': 'Notes',
        'recommended_concentration': 'Recommended concentration',
        'solubility': 'Solubility',
        'physical_state': 'Physical state',
    } 
   
class FormulationIngredientForm(forms.ModelForm):
    class Meta: 
        model = FormulationIngredient
        fields = ["ingredient", "percentage"]

    widgets = {
        'percentage': forms.NumberInput(attrs={'placeholder': 'e.g., 5,00'}),
    }
    labels = {
        'percentage': 'Concentration',
    } 

FormulationIngredientFormSet = inlineformset_factory(
    Formulation, 
    FormulationIngredient,
    form = FormulationIngredientForm,
    extra=1,    
    can_delete=True,
)