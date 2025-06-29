from django.contrib import admin, messages
from django.core.exceptions import ValidationError 
from django.db.models import Sum 
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

    def save_model(self, request, obj, form, change):
        # Save the main Formulation object 
        super().save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        # Save the related objects (inlines)
        super().save_related(request, form, formsets, change)

        # After saving to the DB, check the percentages
        try:
            form.instance.validate_total_percentage()  
        except ValidationError as e:
            self.message_user(request, e.message, level=messages.ERROR)
            raise e
        
    def total_formulation_percentage(self, obj):
        total_percentage = sum(
            fi.percentage for fi in obj.formulationingredient_set.all()
            if fi.percentage is not None
        )
        return f"{total_percentage:.2f}%"
    
    total_formulation_percentage.short_description = "Total %"
