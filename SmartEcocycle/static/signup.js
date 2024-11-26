document.addEventListener("DOMContentLoaded", () => {
    const userBtn = document.getElementById("userBtn");
    const recyclerBtn = document.getElementById("recyclerBtn");
    const signupForm = document.getElementById("signupForm");

    userBtn.addEventListener("click", () => {
        userBtn.classList.add("active");
        recyclerBtn.classList.remove("active");
    });

    recyclerBtn.addEventListener("click", () => {
        recyclerBtn.classList.add("active");
        userBtn.classList.remove("active");
    });

    signupForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const activeRole = userBtn.classList.contains("active") ? "User" : "Recycler Center";
        alert(`Sign up successful as a ${activeRole}`);
    });
});


//Extra Part


document.getElementById("signupForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        name: formData.get("name"),
        email: formData.get("email"),
        dob: formData.get("dob"),
        phone: formData.get("phone"),
        password: formData.get("password")
    };

    try {
        const response = await fetch("/api/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
        } else {
            const errorData = await response.json();
            alert("Signup failed: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Error during signup:", error);
        alert("An error occurred. Please try again later.");
    }
});