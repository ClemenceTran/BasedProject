document.addEventListener("DOMContentLoaded", function () {
  const bars = document.querySelectorAll(".progress");

  bars.forEach(function (bar) {
    const value = bar.getAttribute("data-width");

    if (value !== null && value !== "") {
      bar.style.width = value + "%";
    }
  });
});