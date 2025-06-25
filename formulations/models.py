from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MaxValueValidator, MinValueValidator 


# Create your models here.

class Ingredient(models.Model):
    """
    Represents a single cosmetic ingredient with its properties. 
    Ingredient will be put into the db and shared across all application: every user will be able to use it into his/her formula.
    """
    name = models.CharField(max_length=200, unique=True, help_text="Brand name of the ingredient (e.g., Emulsifying Wax NF)")
    inci_name = models.CharField(max_length=255, blank=False, help_text="INCI name")
   
    # properties for additional information about ingredient 
    functionality = models.CharField(max_length=255, blank=True, null=True, help_text="Primary function (e.g., Emulsifier, Humectant, Preservative)")
    solubility = models.CharField(
        max_length=50,
        choices=[
            ('water', 'Water Soluble'),
            ('oil', 'Oil Soluble'),
            ('dispersible', 'Water Dispersible'),
            ('other', 'Other'),
        ],
        blank=True,
        null=True,
        help_text="Solubility in water or oil."
    )
    physical_state = models.CharField(
        max_length=50,
        choices=[
            ('liquid','Liquid'),
            ('powder', 'Powder'),
            ('pellets','Pellets'),
            ('paste','Paste'),
        ],
        blank=True,
        null=True,
        help_text="Physical state under normal conditions."
    )
    recommended_concentration = models.CharField(max_length=100, blank=True, null=True, help_text="Typical usage percentage range (e.g., '0.5-5%', '10-20%')")
    notes = models.TextField(blank=True, null=True, help_text="Any additional notes or warnings about the ingredient")

    class Meta:
        # Define default ordering for ingredients when queried
        ordering = ['name'] 

    def __str__(self):
        return self.name   
    
class Formulation(models.Model):
    """
    Represents a cosmetic formula.
    Each formulation belongs to a specific user.
    """
    # if user is deleted, all his/her formulations will be deleted as well
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who created this formulation")
    # name of the formula will be unique for the user himself: see class Meta and unique_together
    name = models.CharField(max_length=255, help_text="Name of the formulation (e.g., 'Hydrating Face Cream')")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the formulation")
    batch_size_grams = models.DecimalField(
        max_digits=100,
        decimal_places=2,
        default = 100,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Optional: Target batch size in grams"
    )
    ingredients = models.ManyToManyField(Ingredient, through='FormulationIngredient')

    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the formulation was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the formulation was last updated")
    class Meta:
        ordering = ['-created_at'] # by most recent
        # Ensure a user cannot have two formulations with the exact same name
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name}"


class FormulationIngredient(models.Model):
    """
    A model representing an ingredient within a formulation,
    including its percentage.
    """
    formulation = models.ForeignKey(Formulation, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        # help_text="Percentage of this ingredient in the formula (e.g., 5.00 for 5%)"
    )
    instructions = models.TextField(blank=True, null=True, help_text="Step-by-step instructions for ingredient addition")
    # ensure, that order in which ingredients were inputed, stays the same
    order = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="The order in which to display an ingredient.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.ingredient.name} ({self.percentage}%) in {self.formulation.name} formula."