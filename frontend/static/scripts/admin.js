// scripts/admin.js

document.addEventListener("DOMContentLoaded", (e) => {

  const loginForm = document.getElementById("login-form");
  const loginButton = document.getElementById("login-button");


  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    loginButton.disabled = true;
    loginButton.innerText = "Logging in...";

    const formData = new FormData(loginForm);
    const username = formData.get("username");
    const password = formData.get("password");

    const response = await fetch("/admin/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({username, password}),
    });

    if (response.ok) {
      return window.location.reload();
    } else {
      alert("Login failed.");
      loginButton.disabled = false;
      loginButton.innerText = "Login";
    }
  })
});