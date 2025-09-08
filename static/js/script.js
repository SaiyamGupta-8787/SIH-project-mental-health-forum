// Mobile Navbar
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

hamburger.addEventListener("click", () =>
  navLinks.classList.toggle("show")
);

document.querySelectorAll(".nav-links a").forEach(link =>
  link.addEventListener("click", () => navLinks.classList.remove("show"))
);

// Sidebar toggle
function toggleMenu(header) {
  const submenu = header.nextElementSibling;
  header.querySelector(".arrow").classList.toggle("down");
  submenu.style.maxHeight = submenu.style.maxHeight ? null : submenu.scrollHeight + "px";
}
