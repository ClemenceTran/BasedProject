const micBtn = document.getElementById("micBtn");
const textAnswer = document.getElementById("textAnswer");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";

    micBtn.addEventListener("click", () => {
        recognition.start();
        micBtn.textContent = "🎙 Listening...";
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        textAnswer.value += " " + transcript;
        micBtn.textContent = "🎤 Speak";
    };

    recognition.onerror = () => {
        micBtn.textContent = "🎤 Speak";
    };
} else {
    micBtn.disabled = true;
    micBtn.textContent = "Voice not supported";
}
