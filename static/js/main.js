// Utility functions
function showMessage(elementId, message, type) {
  const element = document.getElementById(elementId)
  if (element) {
    element.textContent = message
    element.className = `message ${type}`
    element.style.display = "block"
  }
}

function hideMessage(elementId) {
  const element = document.getElementById(elementId)
  if (element) {
    element.style.display = "none"
  }
}

// Add smooth scrolling
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({ behavior: "smooth" })
      }
    })
  })
})
