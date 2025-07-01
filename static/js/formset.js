
// console.log("formset.js loaded");
document.addEventListener('DOMContentLoaded', function () {
   
    // create_formulation.html logic
    const addBtn = document.getElementById('add-ingredient');
    if (addBtn) {
        const formsetContainer = document.getElementById('ingredient-formset');
        const totalForms = document.querySelector('#id_form-TOTAL_FORMS');
        addBtn.addEventListener('click', function () {
            // console.log("Add button clicked!");
            const currentFormCount = parseInt(totalForms.value);
            const allForms = formsetContainer.querySelectorAll('.ingredient-form');
            const lastForm = allForms[allForms.length - 1];
            // console.log("lastForm", lastForm);
        
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
            newForm.querySelector('[name$="-percentage-weight"]').textContent = '';

            // Append new line
            formsetContainer.appendChild(newForm);
            totalForms.value = currentFormCount + 1;

            // Added row has delete btn, attached listener for deletion
            bindDeleteButtons();
            bindPercentageSum();
        });
        // Initial binding
        bindDeleteButtons();
        bindPercentageSum();
        updatePercentageSum();
    }


    // profile.html logic
    const deleteButtons = document.querySelectorAll(".deleteButton");
    const deleteForm = document.getElementById("delete-form");

    if (deleteButtons){
        deleteButtons.forEach(button => {
            button.addEventListener("click", () => {
                const formulationId = button.getAttribute("data-formulation-id");
                console.log("formulationId for deleting formula is  ", formulationId);
                deleteForm.action = `/formulations/${formulationId}/delete/`;  // Adjust if your URL is different
            });
        });
    }


    // create ingredient, ajax
    const form = document.getElementById("ingredientModalForm");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (form){
        // prevent browser from reloading after form submission
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            // sending dat via POST method
            fetch("/ingredient/create/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams(new FormData(form))
            })
            // expected response from create_ingredient_view is in json format
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // console.log(data);
                    alert(data.message);

                    // Append new ingredient to all dropdowns in formset
                    document.querySelectorAll("select[name$='-ingredient']").forEach(select => {
                        const option = new Option(data.name, data.id, false, false);
                        select.appendChild(option);
                    });

                    form.reset();  // Reset the modal form
                    document.getElementById("defaultModal").classList.add("hidden"); // Close modal
                } else {
                    console.error(data.errors);
                
                }
            })
            .catch(err => {
                console.error("AJAX error:", err)
                // Error display to the user
                const errorDiv = document.getElementById("ingredientError");
                if (errorDiv) {
                    errorDiv.textContent = "Failed to save ingredient. Please try again.";
                }
            });
        });
    }
});

// row removing
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
    } else {
        console.warn("Delete input not found in row!");
    }
    updatePercentageSum();

}
 // percentage validation
 function updatePercentageSum() {
    let total = 0;
    const percentageInputs = document.querySelectorAll('input[name$="-percentage"]');
    const batchSize = document.getElementById('id_batch_size_grams');
    const valueBatchSize = parseFloat(batchSize.value.replace(',', '.'));

    percentageInputs.forEach(input => {
        const parentDiv = input.closest('div').parentElement; 
        const deleteCheckbox = parentDiv.querySelector('input[name$="-DELETE"]');
        // console.log('deleteCheckbox', deleteCheckbox);
        const value = parseFloat(input.value.replace(',', '.')); // In case user uses comma

        // live weight calculation
        const weight = parentDiv.querySelector('[name$="-percentage-weight"]');
        const weightValue = value/100 * valueBatchSize;
        
        if (!isNaN(value)) {
            total += value;
            weight.textContent = `${weightValue} g`;
            // console.log('checkbox is addded')
            if (deleteCheckbox.value == "on" && deleteCheckbox.checked){
                total -= value;
            }
        }          
    });

    const sumDisplay = document.getElementById("percentage-sum");
    const saveBtn = document.getElementById("save-button");
    saveBtn.disabled = true;

    sumDisplay.textContent = `${total.toFixed(2)}%`;

    if (total >= 99.99 && total <= 100.01) {
        sumDisplay.classList.remove("text-pink-600");
        sumDisplay.classList.add("text-green-600");
        saveBtn.disabled = false;
        saveBtn.classList.remove("opacity-50", "cursor-not-allowed");
    } else {
        sumDisplay.classList.remove("text-green-600");
        sumDisplay.classList.add("text-pink-600");
        saveBtn.disabled = true;
        saveBtn.classList.add("opacity-50", "cursor-not-allowed");
    }
}
    
function bindPercentageSum(){
    const percentageInputs = document.querySelectorAll('input[name$="-percentage"]');
    percentageInputs.forEach(input => {
        input.removeEventListener("input", updatePercentageSum);
        input.addEventListener("input", updatePercentageSum);
    });
    const batchSize = document.getElementById('id_batch_size_grams');
    batchSize.addEventListener("input", updatePercentageSum)
}