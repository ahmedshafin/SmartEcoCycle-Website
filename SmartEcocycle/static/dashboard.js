document.addEventListener("DOMContentLoaded", () => {
    const sideMenu = document.querySelector("aside");
    const menuBtn = document.getElementById("menu-btn");
    const closeBtn = document.getElementById("close-btn");
    const darkMode = document.querySelector(".dark-mode");

    // Set Dark Mode as Default
    document.body.classList.add("dark-mode-variables");  

    // Update Toggle Button to Show Dark Mode is Active
    darkMode.querySelector("span:nth-child(1)").classList.add("active");
    darkMode.querySelector("span:nth-child(2)").classList.remove("active");

    // Open Sidebar Menu
    menuBtn.addEventListener("click", () => {
        sideMenu.style.display = "block";
    });

    // Close Sidebar Menu
    closeBtn.addEventListener("click", () => {
        sideMenu.style.display = "none";
    });

    // Toggle Dark Mode
    darkMode.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode-variables");

        // Update Toggle Button State
        darkMode.querySelector("span:nth-child(1)").classList.toggle("active");
        darkMode.querySelector("span:nth-child(2)").classList.toggle("active");
    });

    // Dummy Orders Array for Table
    Orders.forEach(order => {
        const tr = document.createElement("tr");
        const trContent = `
            <td>${order.productName}</td>
            <td>${order.productNumber}</td>
            <td>${order.paymentStatus}</td>
            <td class="${order.status === 'Declined' ? 'danger' : order.status === 'Pending' ? 'warning' : 'primary'}">${order.status}</td>
            <td class="primary">Details</td>
        `;
        tr.innerHTML = trContent;
        document.querySelector("table tbody").appendChild(tr);
    });
});
