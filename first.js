// script.js

document.getElementById("Submit").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
    // Perform any form validation if needed
    // If validation passes, redirect to the home page
    window.location.href = "{{ url_for('index') }}"; // Redirect to the home page
});
redirectAfterDelay({{ redirect_delay }});
