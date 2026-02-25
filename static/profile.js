document.addEventListener("DOMContentLoaded", () => {
  // ---------- Password modal ----------
  const pwOverlay = document.getElementById("pwModalOverlay");
  const openPwBtn = document.getElementById("openPwModal");
  const closePwBtn = document.getElementById("closePwModal");
  const cancelPwBtn = document.getElementById("cancelPwModal");

  function openPw() {
    if (!pwOverlay) return;
    pwOverlay.classList.add("open");
    pwOverlay.setAttribute("aria-hidden", "false");
  }

  function closePw() {
    if (!pwOverlay) return;
    pwOverlay.classList.remove("open");
    pwOverlay.setAttribute("aria-hidden", "true");
  }

  if (openPwBtn) openPwBtn.addEventListener("click", openPw);
  if (closePwBtn) closePwBtn.addEventListener("click", closePw);
  if (cancelPwBtn) cancelPwBtn.addEventListener("click", closePw);

  if (pwOverlay) {
    pwOverlay.addEventListener("click", (e) => {
      if (e.target === pwOverlay) closePw();
    });
  }

  // Eye toggle
  document.querySelectorAll(".eye[data-eye]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-eye");
      const input = document.getElementById(id);
      if (!input) return;
      input.type = input.type === "password" ? "text" : "password";
    });
  });

  // ---------- Edit info modal ----------
  const infoOverlay = document.getElementById("infoModalOverlay");
  const openEditBtn = document.getElementById("openEditModal");
  const closeInfoBtn = document.getElementById("closeInfoModal");
  const cancelInfoBtn = document.getElementById("cancelInfoModal");
  const infoForm = document.getElementById("infoForm");

  // Track if user changed anything
  let infoDirty = false;

  // Save initial values to compare later
  const initialInfoValues = {};
  if (infoForm) {
    Array.from(infoForm.elements).forEach((el) => {
      if (el.name && (el.tagName === "INPUT" || el.tagName === "TEXTAREA")) {
        initialInfoValues[el.name] = el.value;
      }
    });
  }

  function recomputeDirty() {
    if (!infoForm) return false;
    let dirty = false;
    Array.from(infoForm.elements).forEach((el) => {
      if (!el.name) return;
      if (initialInfoValues.hasOwnProperty(el.name)) {
        if (el.value !== initialInfoValues[el.name]) dirty = true;
      }
    });
    infoDirty = dirty;
    return dirty;
  }

  if (infoForm) {
    infoForm.addEventListener("input", () => {
      recomputeDirty();
    });
  }

  function openInfo() {
    if (!infoOverlay) return;
    infoOverlay.classList.add("open");
    infoOverlay.setAttribute("aria-hidden", "false");
    recomputeDirty();
  }

  function doCloseInfo(force = false) {
    if (!infoOverlay) return;

    if (!force && recomputeDirty()) {
      // for confirm
      const wantSave = window.confirm("You changed information. Do you want to save it?");
      if (wantSave) {
        // submit form
        if (infoForm) infoForm.submit();
        return;
      } else {
        // discard changes: reset to initial values
        if (infoForm) {
          Array.from(infoForm.elements).forEach((el) => {
            if (!el.name) return;
            if (initialInfoValues.hasOwnProperty(el.name)) {
              el.value = initialInfoValues[el.name];
            }
          });
        }
      }
    }

    infoOverlay.classList.remove("open");
    infoOverlay.setAttribute("aria-hidden", "true");
    infoDirty = false;
  }

  if (openEditBtn) openEditBtn.addEventListener("click", openInfo);
  if (closeInfoBtn) closeInfoBtn.addEventListener("click", () => doCloseInfo(false));
  if (cancelInfoBtn) cancelInfoBtn.addEventListener("click", () => doCloseInfo(false));

  if (infoOverlay) {
    infoOverlay.addEventListener("click", (e) => {
      if (e.target === infoOverlay) doCloseInfo(false);
    });
  }

  // ESC closes whichever modal is open
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;

    if (infoOverlay && infoOverlay.classList.contains("open")) {
      doCloseInfo(false);
    } else if (pwOverlay && pwOverlay.classList.contains("open")) {
      closePw();
    }
  });
});