// JavaScript to toggle between displaying profile and edit form
document.addEventListener("DOMContentLoaded", function () {
    const editProfileButton = document.getElementById("editProfile");
    const cancelEditButton = document.getElementById("cancelEdit");
    const saveChangesButton = document.getElementById("saveChanges");

    editProfileButton.addEventListener("click", function () {
        toggleEditForm();
    });

    cancelEditButton.addEventListener("click", function () {
        toggleEditForm();
    });

    saveChangesButton.addEventListener("click", function () {
        // Perform AJAX request to update profile data
        // Update the displayed data
        toggleEditForm();
    });

    function toggleEditForm() {
        const card = document.querySelector(".card");
        const editForm = document.getElementById("editForm");
        const editButtons = document.getElementById("editButtons");

        if (card.style.display === "none" || card.style.display === "") {
            card.style.display = "block";
            editForm.style.display = "none";
            editButtons.style.display = "none";
        } else {
            card.style.display = "none";
            editForm.style.display = "block";
            editButtons.style.display = "block";
        }
    }
});
