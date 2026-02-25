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

  // ---------- Eye toggle (SVG swap) ----------
  const EYE_OFF_SVG = `
    <svg class="eye-icon" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
      <path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/>
      <path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/>
      <path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/>
      <path d="m2 2 20 20"/>
    </svg>
  `;

  const EYE_SVG = `
    <svg class="eye-icon" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
      <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  `;

  // Ensure all eye buttons start with eye-off icon
  document.querySelectorAll(".eye[data-eye]").forEach((btn) => {
    if (!btn.querySelector("svg")) {
      btn.innerHTML = EYE_OFF_SVG;
    }
  });

  document.querySelectorAll(".eye[data-eye]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-eye");
      const input = document.getElementById(id);
      if (!input) return;

      const willShow = input.type === "password";
      input.type = willShow ? "text" : "password";

      // Swap icon
      btn.innerHTML = willShow ? EYE_SVG : EYE_OFF_SVG;
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
      const wantSave = window.confirm("You changed information. Do you want to save it?");
      if (wantSave) {
        if (infoForm) infoForm.submit();
        return;
      } else {
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