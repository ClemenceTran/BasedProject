document.addEventListener("DOMContentLoaded", function () {

    // ---------------- STEP 1: Select Mode ----------------
    const cards = document.querySelectorAll(".mode-card");
    const goStep2 = document.getElementById("goStep2");
    const modeFocus = document.getElementById("modeFocus");

    const focusText = {
        hr: "This interview will focus on HR / behavioral questions.",
        technical: "This interview will focus on your technical abilities."
    };

    let selected = "technical"; // default selection

    function applySelected(type) {
        selected = type;

        // Highlight the selected card
        cards.forEach(btn => {
            btn.classList.toggle("selected", btn.dataset.type === type);
        });

        // Update Start button URL
        if (goStep2) {
            const base = goStep2.dataset.base; // Flask base URL
            goStep2.href = `${base}&type=${type}`; // append selected type
        }

        // Update mode focus text
        if (modeFocus) {
            modeFocus.textContent = focusText[type] || "";
        }
    }

    // Card click handler
    cards.forEach(btn => {
        btn.addEventListener("click", () => applySelected(btn.dataset.type));
    });

    // Initialize default selection
    if (cards.length) applySelected(selected);

    // ---------------- STEP 2: CV Upload Preview ----------------
    const cvInput = document.getElementById("cv");
    const cvName = document.getElementById("cvName");

    if (cvInput && cvName) {
        cvInput.addEventListener("change", () => {
            cvName.textContent = cvInput.files.length ? cvInput.files[0].name : "";
        });

        // Make label clickable to open file picker if input is hidden
        const uploadLabel = document.querySelector("label[for='cv']");
        if (uploadLabel) {
            uploadLabel.addEventListener("click", () => {
                cvInput.click();
            });
        }
    }

    // ---------------- Optional: STEP 2 form submit feedback ----------------
    const interviewForm = document.querySelector(".interview-form");
    if (interviewForm) {
        interviewForm.addEventListener("submit", (e) => {
            // You can add a loader or disable button to prevent double submit
            const startBtn = interviewForm.querySelector(".start-btn");
            if (startBtn) {
                startBtn.disabled = true;
                startBtn.textContent = "Starting...";
            }
        });
    }

});
