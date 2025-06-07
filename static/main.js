// Wait until the page content has fully loaded
document.addEventListener('DOMContentLoaded', function () {

  // Select all elements with the class 'heart-button' (the favorite buttons)
  document.querySelectorAll('.heart-button').forEach(btn => {

    // Add a click event to each button
    btn.addEventListener('click', async function (evt) {
      evt.preventDefault(); // Prevent default form/button behavior

      // Get the dog’s unique ID and check if it's already favorited
      const dogId = btn.dataset.dogId;
      const isFavorited = btn.dataset.favorited === "true";

      // Set the API endpoint: either favorite or unfavorite
      const endpoint = isFavorited ? "/unfavorite" : "/favorite";

      // Build the data to send to the backend
      const payload = {
        dog_id: dogId,
        dog_name: btn.dataset.dogName,
        dog_photo: btn.dataset.dogPhoto,
        dog_url: btn.dataset.dogUrl
      };

      // Send the POST request to the appropriate endpoint
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json(); // Parse the JSON response

      // If the status says dog was added or removed, update the UI
      if (data.status === "added" || data.status === "removed") {
        btn.classList.toggle('filled'); // Toggle the filled heart style
        btn.dataset.favorited = (!isFavorited).toString(); // Update data attribute
        btn.innerHTML = btn.dataset.favorited === "true" ? "❤️" : "🤍"; // Update heart symbol

        // If we're on the favorites page and the dog was unfavorited,
        // fade out and remove the dog card from the page
        if (window.location.pathname === "/favorites" && data.status === "removed") {
          const dogCard = btn.closest(".dog-card");
          if (dogCard) {
            dogCard.classList.add("fade-out");
            setTimeout(() => dogCard.remove(), 400); // Wait for fade animation to complete
          }
        }
      }
    });
  });
});


// Automatically fade out flash messages (e.g. "Account created!", etc.)
document.addEventListener("DOMContentLoaded", function () {
  const flashMessages = document.querySelectorAll(".flash");

  flashMessages.forEach(msg => {
    setTimeout(() => {
      msg.style.display = "none";
    }, 4500); // Hide after 4.5 seconds
  });
});


// Mobile navigation toggle for hamburger menu
document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger'); // Hamburger icon
  const navLinks = document.getElementById('nav-links');  // Collapsible nav

  // Toggle the nav menu when hamburger is clicked
  hamburger.addEventListener('click', function () {
    navLinks.classList.toggle('open');
  });
});
