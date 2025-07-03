document.addEventListener("DOMContentLoaded", function () {
  const email = "ed.korsberg" + "@" + "gmail.com";
  const span = document.getElementById("email");
  if (span) {
    span.innerHTML = `<a href="mailto:${email}">${email}</a>`;
  }
});
