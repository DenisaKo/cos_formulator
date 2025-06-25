
document.addEventListener('DOMContentLoaded', function () {
    const addBtn = document.getElementById('add-ingredient');
    const formsetContainer = document.getElementById('ingredient-formset');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    addBtn.addEventListener('click', function () {
        console.log("Add button clicked!");
        const currentFormCount = parseInt(totalForms.value);
        const formTemplate = document.querySelector('.ingredient-form:last-of-type');
        const newForm = formTemplate.cloneNode(true);

        // Update form fields with new index
        newForm.innerHTML = newForm.innerHTML.replace(/form-(\d+)-/g, `form-${currentFormCount}-`);

        // Clear input values
        newForm.querySelectorAll('input, textarea, select').forEach(input => {
            if (input.type !== 'hidden') input.value = '';
        });

        formsetContainer.appendChild(newForm);
        totalForms.value = currentFormCount + 1;
    });
});
    
