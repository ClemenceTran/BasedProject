document.addEventListener("DOMContentLoaded", () => {
  const step1 = document.getElementById("step1");
  const step2 = document.getElementById("step2");

  const uploadBox = document.getElementById("uploadBox");
  const cvInput = document.getElementById("cvInput");
  const fileName = document.getElementById("fileName");

  const jobDesc = document.getElementById("jobDesc");
  const nextBtn = document.getElementById("nextBtn");

  const backBtn = document.getElementById("backBtn");
  const startBtn = document.getElementById("startBtn");

  const error1 = document.getElementById("error1");
  const error2 = document.getElementById("error2");

  const modeHint = document.getElementById("modeHint");
  const modeCards = document.querySelectorAll(".mode-card");

  let selectedMode = null;

  function showStep(n) {
    if (n === 1) {
      step1.classList.remove("hidden");
      step1.style.display = "block";

      step2.classList.add("hidden");
      step2.style.display = "none";
    } else {
      step1.classList.add("hidden");
      step1.style.display = "none";

      step2.classList.remove("hidden");
      step2.style.display = "block";
    }
  }

  // Upload box -> open file picker
  if (uploadBox && cvInput) {
    uploadBox.addEventListener("click", () => cvInput.click());
    uploadBox.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") cvInput.click();
    });
  }

  // Show filename
  if (cvInput && fileName) {
    cvInput.addEventListener("change", () => {
      const f = cvInput.files && cvInput.files[0] ? cvInput.files[0] : null;
      fileName.textContent = f ? f.name : "No file selected";
    });
  }

  // =========================
  // NEXT button
  // =========================
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      // validation disabled for now
      showStep(2);
    });
  }

  // Mode selection (visual only)
  modeCards.forEach((card) => {
    card.addEventListener("click", () => {
      modeCards.forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      selectedMode = card.dataset.mode;

      if (modeHint) {
        modeHint.textContent =
          selectedMode === "hr"
            ? "Will focus on behavioral and soft skills."
            : "Will focus on technical abilities.";
      }
    });
  });

  // Back
  if (backBtn) {
    backBtn.addEventListener("click", () => showStep(1));
  }

  // =========================
  // START button (UPDATED)
  // =========================
  if (startBtn) {
    startBtn.addEventListener("click", () => {
      console.log("Start clicked"); // debug

      // Take selected mode if clicked, otherwise default to "hr"
      const selectedCard = document.querySelector(".mode-card.selected");
      const mode = selectedCard ? selectedCard.dataset.mode : (selectedMode || "hr");

      // Redirect to interview room with mode
      window.location.href = `/interview-room?mode=${encodeURIComponent(mode)}`;
    });
  }

  // init
  showStep(1);
});