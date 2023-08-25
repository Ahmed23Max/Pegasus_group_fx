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


