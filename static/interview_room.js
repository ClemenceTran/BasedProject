// static/interview_room.js

document.addEventListener("DOMContentLoaded", () => {
  // ---------- DOM ----------
  const chatBox = document.getElementById("chatBox");
  const msgInput = document.getElementById("msgInput");
  const sendBtn = document.getElementById("sendBtn");
  const modeLine = document.getElementById("modeLine");

  // New composer UI
  const textMode = document.getElementById("textMode");
  const recordMode = document.getElementById("recordMode");
  const micBtn = document.getElementById("micBtn");
  const cancelRecBtn = document.getElementById("cancelRecBtn");
  const submitRecBtn = document.getElementById("submitRecBtn");

  // ---------- Mode ----------
  const urlParams = new URLSearchParams(window.location.search);
  const mode = (urlParams.get("mode") || "hr").toLowerCase();

  if (modeLine) {
    modeLine.textContent = "Mode: " + (mode === "technical" ? "Technical" : "HR");
  }

  // ---------- Interview content ----------
  const hrQuestions = [
    "Tell me about yourself.",
    "Why do you want this role?",
    "Describe a time you faced a challenge and how you handled it.",
    "What are your strengths and weaknesses?",
    "Tell me about a time you worked in a team and what your role was.",
  ];

  const techQuestions = [
    "Explain overfitting and two ways to reduce it.",
    "What is the difference between supervised and unsupervised learning?",
    "Explain bias vs variance.",
    "How would you evaluate a classification model?",
    "What is the difference between precision and recall?",
  ];

  const questions = mode === "technical" ? techQuestions : hrQuestions;
  let qIndex = 0;

  // ---------- Helpers ----------
  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function isNearBottom(px = 60) {
    if (!chatBox) return true;
    return chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight < px;
  }

  function scrollToBottom() {
    if (!chatBox) return;
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function appendMessageRow(role /* "ai"|"user" */, html) {
    if (!chatBox) return;

    const shouldFollow = isNearBottom(80);

    const row = document.createElement("div");
    row.className = `msg-row ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";
    bubble.innerHTML = html;

    row.appendChild(bubble);
    chatBox.appendChild(row);

    if (shouldFollow) scrollToBottom();
  }

  function addText(sender, text) {
    const safe = escapeHtml(text);
    const role = sender === "You" ? "user" : "ai";
    appendMessageRow(role, `<strong>${sender}:</strong> ${safe}`);
  }

  function addAudio(sender, blobUrl) {
    const role = sender === "You" ? "user" : "ai";
    appendMessageRow(
      role,
      `<strong>${sender}:</strong>
       <div><audio controls src="${blobUrl}"></audio></div>`
    );
  }

  function askNextQuestion() {
    const q = questions[qIndex % questions.length];
    qIndex += 1;
    addText("AI", q);
  }

  // ---------- Send button state ----------
  function updateSendState() {
    const hasText = (msgInput?.value || "").trim().length > 0;
    if (sendBtn) sendBtn.disabled = !hasText;
  }

  // ---------- Text send ----------
  function handleSendText() {
    const text = (msgInput?.value || "").trim();
    if (!text) return;

    addText("You", text);
    msgInput.value = "";
    updateSendState();

    setTimeout(() => {
      addText("AI", "Got it. Let’s continue.");
      setTimeout(askNextQuestion, 350);
    }, 350);
  }

  // ---------- Record UI helpers ----------
  function enterRecordModeUI() {
    if (textMode) textMode.classList.add("hidden");
    if (recordMode) recordMode.classList.remove("hidden");
    if (msgInput) msgInput.blur();
  }

  function exitRecordModeUI() {
    if (recordMode) recordMode.classList.add("hidden");
    if (textMode) textMode.classList.remove("hidden");
    updateSendState();
    if (msgInput) msgInput.focus();
  }

  // ---------- Voice recording ----------
  let mediaRecorder = null;
  let chunks = [];
  let stream = null;

  // If true: onstop will submit; if false: discard
  let shouldSubmitRecording = false;

  function stopStreamTracks() {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      stream = null;
    }
  }

  async function startRecording() {
    try {
      // Reset state
      shouldSubmitRecording = false;
      chunks = [];

      stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const candidates = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/ogg;codecs=opus",
        "audio/ogg",
      ];

      let mimeType = "";
      for (const t of candidates) {
        if (window.MediaRecorder && MediaRecorder.isTypeSupported(t)) {
          mimeType = t;
          break;
        }
      }

      mediaRecorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        // Always stop mic tracks
        stopStreamTracks();

        // If cancelled: discard and do nothing
        if (!shouldSubmitRecording) return;

        // Submit: create blob + show in chat
        const blob = new Blob(chunks, { type: mediaRecorder.mimeType || "audio/webm" });
        const url = URL.createObjectURL(blob);

        addAudio("You", url);

        setTimeout(() => {
          addText("AI", "Got it. Let’s continue.");
          setTimeout(askNextQuestion, 350);
        }, 350);
      };

      mediaRecorder.start();
      enterRecordModeUI();
    } catch (err) {
      console.error(err);
      alert("Please allow microphone access to record.");
      stopStreamTracks();
      exitRecordModeUI();
    }
  }

  function stopRecording({ submit }) {
    shouldSubmitRecording = !!submit;

    try {
      if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop(); // triggers onstop
      } else {
        // fallback
        stopStreamTracks();
      }
    } catch (e) {
      stopStreamTracks();
    }
  }

  // ---------- Events ----------
  if (sendBtn) sendBtn.addEventListener("click", handleSendText);

  if (msgInput) {
    msgInput.addEventListener("input", updateSendState);

    msgInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleSendText();
      }
    });
  }

  // New mic controls
  if (micBtn) micBtn.addEventListener("click", startRecording);

  if (cancelRecBtn) {
    cancelRecBtn.addEventListener("click", () => {
      // stop + discard
      stopRecording({ submit: false });
      exitRecordModeUI();
    });
  }

  if (submitRecBtn) {
    submitRecBtn.addEventListener("click", () => {
      // stop + submit
      stopRecording({ submit: true });
      exitRecordModeUI();
    });
  }

  // ---------- Init ----------
  updateSendState();
  addText("AI", "Welcome! Your interview is starting now.");
  askNextQuestion();
  setTimeout(scrollToBottom, 0);
});