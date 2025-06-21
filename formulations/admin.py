from django.contrib import admin
from .models import Ingredient, Formulation, FormulationIngredient

# Register your models here.
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin
    list_display = ('name', 'inci_name', 'functionality', 'solubility', 'physical_state', 'recommended_concentration', 'notes')

@admin.register(FormulationIngredient)
class FormulationIngredientAdmin(admin.ModelAdmin):
    list_display = ('formulation', 'ingredient', 'percentage', 'instructions', 'order')

class FormulationIngredientInline(admin.TabularInline):
    model = FormulationIngredient
    extra = 1 # Number of empty forms to display by default
    fields = ('formulation', 'ingredient', 'percentage', 'instructions', 'order')
    # Allows navigating to Phase admin from Formulation admin, as a link
    show_change_link = True  

@admin.register(Formulation)
class FormulationAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin
    list_display = ('name', 'user')
    inlines = [FormulationIngredientInline]