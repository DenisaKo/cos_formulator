from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from formulations.forms import RegistrationForm, FormulationForm, IngredientForm, FormulationIngredientForm, FormulationIngredientFormSet
from formulations.models import Formulation

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) # Log the new user in immediately after registration
            return redirect('home')
    else:
        form = RegistrationForm() # An empty form for GET requests

    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_formulation_view(request):

    if request.method == 'POST':
        # print("Submitted POST data:", request.POST)
        form = FormulationForm(request.POST)
        # ingredient_formset = FormulationIngredientFormSet(request.POST, prefix='form') 
        
        if form.is_valid():
            # When creating a NEW formulation, the instance of it won't exist yet for the FormSet until the Formulation is saved. 
            formulation = form.save(commit=False) 
            formulation.user = request.user # Set the user
            formulation.save() 
            # formulation must exist - to has pk for PhaseFormSet
            ingredient_formset = FormulationIngredientFormSet(request.POST, instance=formulation, prefix='form')

            if ingredient_formset.is_valid():
                ingredient_formset.save()
                return redirect('formulation_list')
                
            else:
                # If phase formset fails, delete the parent formulation that was just saved.
                formulation.delete()
    else:
        form = FormulationForm()
        ingredient_formset = FormulationIngredientFormSet(prefix='form')

    context = {
        'form': form, 
        'ingredient_formset': ingredient_formset, 
    }
    return render(request, 'formulations/create_formulation.html', context)

@login_required
def edit_formulation_view(request, pk):
    formulation = get_object_or_404(Formulation, pk=pk, user=request.user)

    if request.method == 'POST':
        form = FormulationForm(request.POST, instance=formulation)
        ingredient_formset = FormulationIngredientFormSet(request.POST, instance=formulation, prefix='form')

        if form.is_valid():
            # print("form is valid")
            form.save()
            if ingredient_formset.is_valid():
                # print("ingredient_formset is valid")
                ingredient_formset.save()
                return redirect('formulation_list') 
                # for ingredient_form in ingredient_formset:
                #     print(ingredient_form.cleaned_data)
        else: 
            print("Formset errors:", ingredient_formset.errors)
        
    else:
        form = FormulationForm(instance=formulation)
        ingredient_formset = FormulationIngredientFormSet(instance=formulation, prefix='form')

    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'formulation': formulation,
    }
    return render(request, 'formulations/create_formulation.html', context)

@login_required
def profile_view(request):
    user_formulations = Formulation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'formulations': user_formulations})

@login_required
def delete_formulation_view(request, pk):
    formulation = get_object_or_404(Formulation, pk=pk, user=request.user)
    if request.method == 'POST':
        print("deleting formulation, ",  formulation)
        formulation.delete()
    return redirect('profile') 