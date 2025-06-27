
console.log("formset.js loaded");
document.addEventListener('DOMContentLoaded', function () {
    const addBtn = document.getElementById('add-ingredient');
    if (!addBtn) {
        console.warn("Add button with id 'add-ingredient' not found!");
        return;
    }
    const formsetContainer = document.getElementById('ingredient-formset');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');


    addBtn.addEventListener('click', function () {
        // console.log("Add button clicked!");
        const currentFormCount = parseInt(totalForms.value);
        const allForms = formsetContainer.querySelectorAll('.ingredient-form');
        const lastForm = allForms[allForms.length - 1];
        console.log("lastForm", lastForm);
    
        const newForm = lastForm.cloneNode(true);
        newForm.style.display = 'block';

        // Update form fields with new index
        newForm.innerHTML = newForm.innerHTML.replace(/form-(\d+)-/g, `form-${currentFormCount}-`);
        // Replace all instances of the previous index with the new index
        newForm.innerHTML = newForm.innerHTML.replace(/id_form-(\d+)-/g, `id_form-${currentFormCount}-`);

        // Clear input values, to be empty for new user input
        newForm.querySelectorAll('input, textarea, select').forEach(input => {
            if (input.type !== 'hidden') input.value = '';
        });

        // Append new line
        formsetContainer.appendChild(newForm);
        totalForms.value = currentFormCount + 1;

        // Added row has delete btn, attached listener for deletion
        bindDeleteButtons();
    });

    function bindDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.delete-row-btn');

        deleteButtons.forEach(btn => {
            btn.removeEventListener('click', handleDelete); // remove previous binding if any
            btn.addEventListener('click', handleDelete);
        });
    }

    function handleDelete(event) {
        const button = event.target;
        const formRow = button.closest('.ingredient-form');
        // console.log("Delete button clicked", formRow);
        const deleteField = formRow.querySelector('input[name$="-DELETE"]');
        console.log("Found delete field:", deleteField);

        if (deleteField) {
            // tells Django to check the checkbox/input for deletion
            console.log("Before:", deleteField.checked); // false
            deleteField.checked = true;
        
            if (!deleteField.checked) deleteField.click();
            console.log("After:", deleteField.checked);  // true

            deleteField.value = "on";
            // hide from the user
            formRow.style.display = 'none';
            // document.querySelectorAll('input[name$="-DELETE"]').forEach(input => {
            //     console.log(input.name, input.checked);
            // });
        } else {
            console.warn("Delete input not found in row!");
        }
    }
    // Initial binding
    bindDeleteButtons();
});


    
