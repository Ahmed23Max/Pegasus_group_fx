// JavaScript to toggle between displaying profile and edit form
document.addEventListener("DOMContentLoaded", function () {
    const editProfileButton = document.getElementById("editProfile");
    const cancelEditButton = document.getElementById("cancelEdit");
    const saveChangesButton = document.getElementById("saveChanges");
    const profileForm = document.getElementById("profileForm");

    editProfileButton.addEventListener("click", function () {
        toggleEditForm();
    });

    cancelEditButton.addEventListener("click", function () {
        toggleEditForm();
    });

    saveChangesButton.addEventListener("click", function () {
        // Serialize the form data into a JSON object
        const formData = new FormData(profileForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Send an AJAX request to update the profile data
        fetch("/update_profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((result) => {
            if (result.message === "Profile updated successfully!") {
                // Profile updated successfully, toggle the form
                toggleEditForm();
            } else {
                // Handle errors or display a message to the user
                console.error("Profile update failed:", result.message);
            }
        })
        .catch((error) => {
            console.error("An error occurred:", error);
        });
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
