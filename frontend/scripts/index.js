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