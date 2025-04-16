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

const resend_btn = document.getElementById("resend-btn");


document.getElementById("ticket-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const email = e.target.email.value;
  const name = e.target.name.value;
  const phone = e.target.phone.value;

  const amount = ticketCount * ticket_price * 100; // Convert to kobo
  alert(amount);

  const handler = PaystackPop.setup({
    key: "pk_test_b5eec36691f6be396e16b71518b13cef5193c7b2", // Replace with your Paystack public key
    email: email,
    amount: amount,
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

  resend_btn.disabled = true;
  resend_btn.innerText = "SENDING...";

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
  .then(response => {
  if (!response.ok) {
    // If the response status code isn't in the 200–299 range, it's an error
    return Promise.reject(new Error(`HTTP error! Status: ${response.status}`));
  }
  return response.json(); // Proceed to parse JSON if the response is OK
})
.then(data => {
  // Handle success response
  if (data.message) {
    alert(data.message);
  } else {
    resend_btn.disabled = false;
    resend_btn.innerText = "RESEND";

  }
})
.catch(error => {
  // Catch any error (network issue, bad response, etc.)
  resend_btn.disabled = false;
  resend_btn.innerText = "RESEND";
  alert('No tickets with this email address');
  console.error(error); // Log the error for debugging
});
});

