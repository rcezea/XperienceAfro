// Dynamic Copyright Date

document.getElementById('year').innerText = new Date().getFullYear().toString();


// Gate Ticket Counter Logic
let gateCount = 1;
const gateCounter = document.getElementById("gate-ticket-count");

document.getElementById("gate-increase-qty").addEventListener("click", () => {
  gateCount++;
  gateCounter.textContent = gateCount;
});

document.getElementById("gate-decrease-qty").addEventListener("click", () => {
  if (gateCount > 1) {
    gateCount--;
    gateCounter.textContent = gateCount;
  }
});

const ticket_sale_button = document.getElementById("ticket_sale_button");

// Gate Ticket Sale Form Submission
document.getElementById("gate-sales-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  ticket_sale_button.disabled = true;
  ticket_sale_button.innerText = "Please wait..."

  const name = this["gate-name"].value;
  const email = this["gate-email"].value;
  const phone = this["gate-phone"].value;

  try {
    const response = await fetch("/tickets/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "same-origin", // sends cookies for session auth
      body: JSON.stringify({
        name,
        email,
        phone,
        quantity: gateCount,
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to generate ticket(s)");
    }

    alert(data.message); // Optional: show issued ticket codes too
  } catch (err) {
    alert("Error: " + err.message);
  }

  // Reset form
  this.reset();
  gateCount = 1;
  gateCounter.textContent = 1;
  ticket_sale_button.disabled = false;
  ticket_sale_button.innerText = "Confirm Sale";
});


// QR Scanner Logic
const qrTextInput = document.getElementById("qr-text");
const qrReader = new Html5Qrcode("qr-reader");
const qrConfig = { fps: 10, qrbox: 250 };

document.getElementById("start-scanner").addEventListener("click", () => {
  Html5Qrcode.getCameras().then(devices => {
    if (devices && devices.length) {
      qrReader.start(devices[0].id, qrConfig, (decodedText) => {
        qrTextInput.value = decodedText;
        qrReader.stop().catch(err => console.error("Failed to stop after scan", err));
      });
    }
  }).catch(err => console.error("Camera access error:", err));
});

document.getElementById("stop-scanner").addEventListener("click", () => {
  qrReader.stop().catch(err => console.error("Stop failed", err));
});

const used_ticket_button = document.getElementById("ticket-used-button");

document.getElementById("scanner-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  used_ticket_button.disabled = true;
  used_ticket_button.innerText = "Checking...";

  const code = qrTextInput.value.trim();
  if (!code) {
    alert("Please scan a QR code first.");
    used_ticket_button.disabled = false;
    used_ticket_button.innerText = "Mark as Used";
    return;
  }

  try {
    const response = await fetch("/tickets/scan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "same-origin", // Important: include session cookie
      body: JSON.stringify({ ticket: code })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ticket scan failed");
    }

    alert(data.message);
  } catch (err) {
    alert("Error: " + err.message);
  }


  qrTextInput.value = "";
  used_ticket_button.disabled = false;
  used_ticket_button.innerText = "Mark as Used";
});
