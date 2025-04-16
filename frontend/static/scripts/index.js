// Dynamic Copyright Date

document.getElementById('year').innerText = new Date().getFullYear().toString();


// Group ticket counter logic
let ticketCount = 2;
const counterDisplay = document.getElementById("group-counter");
const decreaseBtn = document.getElementById("decrease-btn");
const increaseBtn = document.getElementById("increase-btn");

decreaseBtn.addEventListener("click", () => {
  if (ticketCount > 1) {
    ticketCount--;
    counterDisplay.textContent = ticketCount;
  }
});

increaseBtn.addEventListener("click", () => {
  ticketCount++;
  counterDisplay.textContent = ticketCount;
});

document.getElementById("ticket-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const email = e.target.email.value;
  const name = e.target.name.value;
  const phone = e.target.phone.value;
  const amount = ticketCount * 5000 * 100; // Convert to kobo

  const handler = PaystackPop.setup({
    key: "pk_test_b5eec36691f6be396e16b71518b13cef5193c7b2", // Replace with your Paystack public key
    email: email,
    amount: 7000,
    metadata: {
      custom_fields: [
        { display_name: "Name", variable_name: "name", value: name },
        { display_name: "Phone", variable_name: "phone", value: phone },
        { display_name: "Tickets", variable_name: "count", value: ticketCount }
      ]
    },
    callback: function (response) {
      alert("Payment complete! Check your email for tickets.");
    },
    onClose: function () {
      alert("Payment cancelled.");
    }
  });

  handler.openIframe();
});


// Resend ticket

document.getElementById('resend-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const email = document.getElementById('resend-email').value;

  // Simple email validation regex
  const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

  // Check if the email format is valid
  if (!emailRegex.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }

  // Prepare the data to send to the API
  const requestData = {
    email: email
  };

  // Make the API call
  fetch('/tickets/resend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestData),
  })
  .then(response => response.json())
  .then(data => {
    // Check if the API returned a success message
    if (data.message) {
      alert(data.message);
    } else {
      alert('No tickets with this email address');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to resend your ticket. Please try again later.');
  });
});

