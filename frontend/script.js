const BASE_URL = "https://api.devsandengineers.ai/api";

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");
  const updateForm = document.getElementById("updateForm");
  const uploadForm = document.getElementById("uploadForm");

  // Register
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);
      const data = Object.fromEntries(formData.entries());

      const res = await fetch(`${BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      alert(result.message);
    });
  }

  // Login
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const data = Object.fromEntries(formData.entries());

      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      if (res.ok) {
        localStorage.setItem("token", result.data.token);
        window.location.href = "profile.html";
      } else {
        alert(result.message);
      }
    });
  }

  // Load Profile
  const token = localStorage.getItem("token");
  if (document.getElementById("profile") && token) {
    fetch(`${BASE_URL}/user/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((result) => {
        const user = result.data;
        document.getElementById("profile").innerHTML = `
          <p><strong>Name:</strong> ${user.name}</p>
          <p><strong>Email:</strong> ${user.email}</p>
          ${
            user.profilePictureUrl
              ? `<img src="${user.profilePictureUrl}" width="100" />`
              : ""
          }
        `;
      });
  }

  // Update Profile
  if (updateForm && token) {
    updateForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(updateForm);
      const data = Object.fromEntries(formData.entries());

      const res = await fetch(`${BASE_URL}/user/profile`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      alert(result.message);
      location.reload();
    });
  }

  // Upload Picture
  if (uploadForm && token) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(uploadForm);

      const res = await fetch(`${BASE_URL}/user/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await res.json();
      alert(result.message);
      location.reload();
    });
  }
});
