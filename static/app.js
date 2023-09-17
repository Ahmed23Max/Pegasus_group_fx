// JavaScript to toggle between displaying profile and edit form
document.addEventListener("DOMContentLoaded", function () {
    const editProfileButton = document.getElementById("editProfile");
    const cancelEditButton = document.getElementById("cancelEdit");
    const saveChangesButton = document.getElementById("saveChanges");
    const profileForm = document.getElementById("profileForm");
    const dateOfBirthInput = document.getElementById("date_of_birth");
    const countrySelect = document.getElementById("country");
    const phoneNumberInput = document.getElementById("phone_number");

    // Add 27 more countries with their respective phone regions
    const countryToPhoneRegion = {
        "USA": "+1",
        "Canada": "+1",
        "United Kingdom": "+44",
        "Germany": "+49",
        "France": "+33",
        "Australia": "+61",
        "Japan": "+81",
        "India": "+91",
        "Brazil": "+55",
        "Mexico": "+52",
        "China": "+86",
        "Russia": "+7",
        "South Korea": "+82",
        "Italy": "+39",
        "Spain": "+34",
        "Netherlands": "+31",
        "Sweden": "+46",
        "Norway": "+47",
        "Denmark": "+45",
        "Finland": "+358",
        "Switzerland": "+41",
        "Austria": "+43",
        "Belgium": "+32",
        "Greece": "+30",
        "Portugal": "+351",
        "Ireland": "+353",
        "New Zealand": "+64",
    };

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

        // Check if the selected date of birth is at least 18 years ago
        const dob = new Date(dateOfBirthInput.value);
        const now = new Date();
        const age = now.getFullYear() - dob.getFullYear();
        if (age < 18) {
            alert("You must be at least 18 years old to update your profile.");
            return;
        }

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

    // Update phone region based on the selected country
    countrySelect.addEventListener("change", function () {
        const selectedCountry = countrySelect.value;
        const phoneRegion = countryToPhoneRegion[selectedCountry] || "";
        phoneNumberInput.value = phoneRegion;
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
const scrollingTestimonials = document.querySelector('.scrolling-testimonials');

// Duplicate testimonials for scrolling effect
scrollingTestimonials.innerHTML += scrollingTestimonials.innerHTML;

// Scroll the testimonials
let scrollAmount = 0;
const scrollSpeed = 2;

function scrollTestimonials() {
    if (scrollAmount >= scrollingTestimonials.scrollWidth / 2) {
        scrollAmount = 0;
    } else {
        scrollAmount += scrollSpeed;
    }
    scrollingTestimonials.style.transform = `translateX(-${scrollAmount}px)`;
}

setInterval(scrollTestimonials, 30);