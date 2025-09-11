document.addEventListener("DOMContentLoaded", () => {
  // Mobile Navbar
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
      navLinks.classList.toggle("show");
    });

    document.querySelectorAll(".nav-links a").forEach(link => {
      link.addEventListener("click", () => navLinks.classList.remove("show"));
    });
  }

  // Sidebar toggle
  function toggleMenu(header) {
    const submenu = header.nextElementSibling;
    const arrow = header.querySelector(".arrow");
    if (submenu && arrow) {
      arrow.classList.toggle("down");
      submenu.style.maxHeight = submenu.style.maxHeight ? null : submenu.scrollHeight + "px";
    }
  }

  // Make toggleMenu globally accessible for onclick in HTML
  window.toggleMenu = toggleMenu;
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const response = await fetch('/login', { method: 'POST', body: formData });

  const result = await response.json();
  if (response.ok) {
    alert(result.message); // show success message
    setTimeout(() => {
      window.location.href = result.redirect;
    }, 1500); // redirect after 1.5s
  } else {
    alert(result.error);
  }
});
