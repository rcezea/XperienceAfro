// Dynamic Copyright Date

document.getElementById('year').innerText = new Date().getFullYear().toString();


// Group ticket counter logic
let groupCounter = 2; // Start with 2 as the default value

const groupCounterDisplay = document.getElementById('group-counter');
const increaseBtn = document.getElementById('increase-btn');
const decreaseBtn = document.getElementById('decrease-btn');
const buyNowBtn = document.getElementById('group-ticket-btn');

// Function to update the Buy Now button status
function updateBuyNowButton() {
  if (groupCounter < 2) {
    buyNowBtn.disabled = true;
  } else {
    buyNowBtn.disabled = false;
  }
}

// Decrease button functionality
decreaseBtn.addEventListener('click', function() {
  if (groupCounter > 1) { // Ensure it doesn't go below 1
    groupCounter--;
    groupCounterDisplay.innerText = groupCounter;
    updateBuyNowButton();
  }
});

// Increase button functionality
increaseBtn.addEventListener('click', function() {
  groupCounter++;
  groupCounterDisplay.innerText = groupCounter;
  updateBuyNowButton();
});

// Initialize the button state on load
updateBuyNowButton();