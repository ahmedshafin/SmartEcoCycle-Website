document.addEventListener("DOMContentLoaded", () => {
    const showFormBtn = document.getElementById("show-form-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const recyclerForm = document.getElementById("recycler-form");
    const form = document.getElementById("recyclerForm");

    // Get CSRF token from hidden input
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Show Form
    showFormBtn.addEventListener("click", () => {
        recyclerForm.style.display = "block";
    });

    // Hide Form
    cancelBtn.addEventListener("click", () => {
        recyclerForm.style.display = "none";
        form.reset();
    });

    // Handle Form Submission
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const recyclerData = {
            name: document.getElementById("name").value,
            contact_number: document.getElementById("contact_number").value,
            assigned_area: document.getElementById("assigned_area").value,
            status: document.getElementById("status").value
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/api/recyclers/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken  // Add CSRF token in headers
                },
                body: JSON.stringify(recyclerData)
            });

            if (response.ok) {
                alert("Recycler added successfully!");
                recyclerForm.style.display = "none";
                form.reset();
            } else {
                alert("Error adding recycler.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Server error, please try again.");
        }
    });
});
