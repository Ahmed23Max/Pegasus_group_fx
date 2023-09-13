 // JavaScript to toggle between displaying profile and edit form
    document.getElementById("editDateOfBirth").addEventListener("click", function () {
        toggleEditForm("dateOfBirth");
    });

    document.getElementById("editLocation").addEventListener("click", function () {
        toggleEditForm("location");
    });

    document.getElementById("editPhoneNumber").addEventListener("click", function () {
        toggleEditForm("phoneNumber");
    });

    document.getElementById("cancelEdit").addEventListener("click", function () {
        toggleEditForm();
    });

    document.getElementById("profileForm").addEventListener("submit", function (e) {
        e.preventDefault();
        // Perform AJAX request to update profile data
        // Update the displayed data
        toggleEditForm();
    });

    function toggleEditForm(fieldToEdit = "") {
        const card = document.querySelector(".card");
        const editForm = document.getElementById("editForm");

        if (fieldToEdit) {
            // Display the edit form for the selected field
            const fieldElement = document.getElementById(fieldToEdit);
            const fieldInput = document.getElementById(fieldToEdit.toLowerCase());
            fieldInput.value = fieldElement.innerText.trim();
            card.style.display = "none";
            editForm.style.display = "block";
        } else {
            // Display the profile card and hide the edit form
            card.style.display = "block";
            editForm.style.display = "none";
        }
    }
