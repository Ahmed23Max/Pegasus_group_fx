$(document).ready(function () {
    $(".navbar-toggler").click(function () {
        $(".mobile-overlay").fadeToggle(); // Toggle the overlay
        $("body").toggleClass("no-scroll"); // Prevent scrolling on background
    });

    // Close the overlay when clicking anywhere on it
    $(".mobile-overlay").click(function () {
        $(this).fadeOut();
        $("body").removeClass("no-scroll");
    });
});




const cardCarousel = document.querySelector('.card-carousel');
  const cards = document.querySelectorAll('.card');
  const description = document.querySelector('.description');
  const button = document.querySelector('.button');
  const leftArrow = document.getElementById('leftArrow');
  const rightArrow = document.getElementById('rightArrow');

  let currentCardIndex = 0;

  function updateDescription() {
    description.innerHTML = `
      <h2>${cards[currentCardIndex].innerText}</h2>
      <p>This is the description for ${cards[currentCardIndex].innerText} option.</p>
    `;
  }

  function updateUI() {
    updateDescription();
  }

  leftArrow.addEventListener('click', () => {
    currentCardIndex = (currentCardIndex - 1 + cards.length) % cards.length;
    updateUI();
    updateCardCarousel();
  });

  rightArrow.addEventListener('click', () => {
    currentCardIndex = (currentCardIndex + 1) % cards.length;
    updateUI();
    updateCardCarousel();
  });

  function updateCardCarousel() {
    cardCarousel.style.transform = `translateX(${-currentCardIndex * 420}px)`; // Adjusted for card width and margin
  }

  cards.forEach((card, index) => {
    card.addEventListener('click', () => {
      currentCardIndex = index;
      updateUI();
      updateCardCarousel();
    });
  });

  button.addEventListener('click', () => {
    // Handle the selection here
  });

  // Initialize the UI
  updateUI();

const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const paymentBox = document.getElementById('payment-box');
const payButton = document.getElementById('pay-button');

loginButton.addEventListener('click', () => {
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
    paymentBox.style.display = 'none';
});

signupButton.addEventListener('click', () => {
    signupForm.style.display = 'block';
    loginForm.style.display = 'none';
    paymentBox.style.display = 'none';
});

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    paymentBox.style.display = 'block';
});

signupForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const signupEmail = document.getElementById('signup-email');
    const errorDiv = document.getElementById('signup-error');

    if (signupEmail.value === "") {
        errorDiv.textContent = "Please enter your email address.";
        return;
    }
    errorDiv.textContent = "";
    paymentBox.style.display = 'block';
});

payButton.addEventListener('click', async () => {
    try {
        await simulatePaymentProcessing();
        alert('Payment successful!');
    } catch (error) {
        alert('Payment failed. Please try again.');
    }
});

async function simulatePaymentProcessing() {
    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    // Simulate successful payment
    // Replace this with actual payment processing logic
}

window.addEventListener('load', () => {
    // Check for initial form validation
    paymentBox.dispatchEvent(new Event('input'));
});

// Initial state: Hide all forms and payment box
loginForm.style.display = 'none';
signupForm.style.display = 'none';
paymentBox.style.display = 'none';

