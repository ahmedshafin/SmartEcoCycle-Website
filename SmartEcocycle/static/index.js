document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("show-login").addEventListener("click", function () {
    document.querySelector(".popup").classList.add("active");
  });

  document.querySelector(".close-btn").addEventListener("click", function () {
    document.querySelector(".popup").classList.remove("active");
  });

  window.addEventListener("click", function (e) {
    if (e.target == document.querySelector(".popup")) {
      document.querySelector(".popup").classList.remove("active");
    }
  });
});

const map = L.map("map").setView([51.505, -0.09], 13); // Default location (London)

// Use OpenStreetMap tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Function to update the map based on user input
function updateMap() {
  const address = document.getElementById("address").value;

  if (address.trim() === "") {
    alert("Please enter a valid address");
    return;
  }

  // Geocode the address using OpenStreetMap's Nominatim API
  fetch(
    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
      address
    )}`
  )
    .then((response) => response.json())
    .then((data) => {
      if (data.length > 0) {
        const { lat, lon } = data[0];
        map.setView([lat, lon], 14);

        // Add a marker for the searched address
        L.marker([lat, lon])
          .addTo(map)
          .bindPopup(`<b>Recycling Center near:</b><br>${address}`)
          .openPopup();
      } else {
        alert("Address not found. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Unable to fetch location data.");
    });
}



//Login authentication
document.querySelector("form").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (email && password) {
    fetch("/api/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: email, password: password }),
    })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "Login successful") {
        if (data.role === "user") {
          window.location.href = "/user.html";
        } else if (data.role === "recycler") {
          window.location.href = "/recycler_dashboard.html";
        } else {
          alert("Role not recognized.");
        }
      } else {
        alert(data.message || "Login failed");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred during login.");
    });
  } else {
    alert("Please enter both email and password.");
  }
});


