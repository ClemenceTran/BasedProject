document.addEventListener("DOMContentLoaded", () => {
  const passModal = document.getElementById("passModal");
  const editModal = document.getElementById("editModal");

  const openChangePassword = document.getElementById("openChangePassword");
  const openEditName = document.getElementById("openEditName");

  function openModal(el) {
    if (!el) return;
    el.classList.add("open");
    el.setAttribute("aria-hidden", "false");
  }

  function closeModal(el) {
    if (!el) return;
    el.classList.remove("open");
    el.setAttribute("aria-hidden", "true");
  }

  // Openers
  if (openChangePassword) {
    openChangePassword.addEventListener("click", () => openModal(passModal));
  }

  if (openEditName) {
    openEditName.addEventListener("click", () => openModal(editModal));
  }

  // Close buttons
  document.querySelectorAll("[data-close]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-close");
      closeModal(document.getElementById(id));
    });
  });

  // Click outside to close
  [passModal, editModal].forEach((m) => {
    if (!m) return;
    m.addEventListener("click", (e) => {
      if (e.target === m) closeModal(m);
    });
  });

  // ESC to close
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeModal(passModal);
      closeModal(editModal);
    }
  });
});