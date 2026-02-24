// static/interview_room.js

document.addEventListener("DOMContentLoaded", () => {
  // ---------- DOM ----------
  const chatBox = document.getElementById("chatBox");
  const msgInput = document.getElementById("msgInput");
  const sendBtn = document.getElementById("sendBtn");

  const recordBtn = document.getElementById("recordBtn");
  const stopBtn = document.getElementById("stopBtn");
  const recStatus = document.getElementById("recStatus");

  const backTopBtn = document.getElementById("backTopBtn");
  const modeLine = document.getElementById("modeLine");

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

  // Are we near the bottom? (used to auto-follow newest)
  function isNearBottom(px = 60) {
    if (!chatBox) return true;
    return chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight < px;
  }

  // Scroll to bottom (used after we add new messages)
  function scrollToBottom() {
    if (!chatBox) return;
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function appendMessageRow(role /* "ai"|"user" */, html) {
    if (!chatBox) return;

    // Only auto-scroll if user is already near the bottom
    const shouldFollow = isNearBottom(80);

    const row = document.createElement("div");
    row.className = `msg-row ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";
    bubble.innerHTML = html;

    row.appendChild(bubble);
    chatBox.appendChild(row);

    if (shouldFollow) {
      scrollToBottom();
    }
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

  function handleSendText() {
    const text = (msgInput?.value || "").trim();
    if (!text) return;

    addText("You", text);
    msgInput.value = "";

    setTimeout(() => {
      addText("AI", "Got it. Let’s continue.");
      setTimeout(askNextQuestion, 350);
    }, 350);
  }

  // ---------- Voice recording ----------
  let mediaRecorder = null;
  let chunks = [];
  let stream = null;

  function setRecUI(isRecording) {
    if (recordBtn) recordBtn.disabled = isRecording;
    if (stopBtn) stopBtn.disabled = !isRecording;
    if (recStatus) recStatus.textContent = isRecording ? "Mic: recording..." : "Mic: idle";
  }

  async function startRecording() {
    try {
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

      chunks = [];
      mediaRecorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: mediaRecorder.mimeType || "audio/webm" });
        const url = URL.createObjectURL(blob);

        addAudio("You", url);

        if (stream) {
          stream.getTracks().forEach((t) => t.stop());
          stream = null;
        }

        setTimeout(() => {
          addText("AI", "Got it. Let’s continue.");
          setTimeout(askNextQuestion, 350);
        }, 350);
      };

      mediaRecorder.start();
      setRecUI(true);
    } catch (err) {
      console.error(err);
      if (recStatus) recStatus.textContent = "Mic: blocked";
      alert("Please allow microphone access to record.");
      setRecUI(false);
    }
  }

  function stopRecording() {
    try {
      if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
      }
    } catch (e) {}
    setRecUI(false);
  }

  // ---------- Back button (end interview immediately) ----------
  if (backTopBtn) {
    backTopBtn.addEventListener("click", () => {
      try {
        if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop();
        if (stream) stream.getTracks().forEach((t) => t.stop());
      } catch (e) {}

      window.location.href = "/interview";
    });
  }

  // ---------- Events ----------
  if (sendBtn) sendBtn.addEventListener("click", handleSendText);

  if (msgInput) {
    msgInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") handleSendText();
    });
  }

  if (recordBtn) recordBtn.addEventListener("click", startRecording);
  if (stopBtn) stopBtn.addEventListener("click", stopRecording);

  // ---------- Init ----------
  setRecUI(false);
  addText("AI", "Welcome! Your interview is starting now.");
  askNextQuestion();

  // Start view at bottom
  setTimeout(scrollToBottom, 0);
});