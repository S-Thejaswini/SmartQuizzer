let quizData = []
let currentQuestion = 0
let userAnswers = []
let quizTopic = ""

// Load quiz data
function loadQuiz() {
  const storedQuiz = sessionStorage.getItem("currentQuiz")
  quizTopic = sessionStorage.getItem("quizTopic") || "Quiz"

  if (!storedQuiz) {
    window.location.href = "/"
    return
  }

  quizData = JSON.parse(storedQuiz)
  userAnswers = new Array(quizData.length).fill(null)

  document.getElementById("quizTopic").textContent = quizTopic
  displayQuestion()
}

// Display current question
function displayQuestion() {
  const question = quizData[currentQuestion]
  const optionsContainer = document.getElementById("optionsContainer")
  const feedbackContainer = document.getElementById("feedbackContainer")

  // Update question counter and progress
  document.getElementById("questionCounter").textContent = `Question ${currentQuestion + 1} of ${quizData.length}`

  const progress = ((currentQuestion + 1) / quizData.length) * 100
  document.getElementById("progressFill").style.width = `${progress}%`

  // Display question
  document.getElementById("questionText").textContent = question.question

  // Display options
  const labels = ["A", "B", "C", "D"]
  optionsContainer.innerHTML = question.options
    .map(
      (option, index) => `
        <button class="option-btn" data-index="${index}">
            <span class="option-label">${labels[index]}</span>
            <span class="option-text">${option}</span>
        </button>
    `,
    )
    .join("")

  // Hide feedback
  feedbackContainer.style.display = "none"

  // Add click handlers
  document.querySelectorAll(".option-btn").forEach((btn) => {
    btn.addEventListener("click", () => selectOption(Number.parseInt(btn.dataset.index)))
  })

  // Update buttons
  updateButtons()

  // Restore previous answer if exists
  if (userAnswers[currentQuestion] !== null) {
    showFeedback(userAnswers[currentQuestion])
  }
}

// Select an option
function selectOption(index) {
  // Remove previous selection
  document.querySelectorAll(".option-btn").forEach((btn) => {
    btn.classList.remove("selected")
  })

  // Add selection to clicked option
  document.querySelectorAll(".option-btn")[index].classList.add("selected")

  // Enable submit button
  document.getElementById("submitBtn").disabled = false

  // Store temporary selection
  window.tempSelection = index
}

// Submit answer
function submitAnswer() {
  if (window.tempSelection === undefined) return

  const selectedIndex = window.tempSelection
  userAnswers[currentQuestion] = selectedIndex

  showFeedback(selectedIndex)

  // Disable options after submission
  document.querySelectorAll(".option-btn").forEach((btn) => {
    btn.disabled = true
  })

  document.getElementById("submitBtn").style.display = "none"
  document.getElementById("nextBtn").style.display = "inline-block"

  delete window.tempSelection
}

// Show feedback
function showFeedback(selectedIndex) {
  const question = quizData[currentQuestion]
  const correctIndex = question.correct_answer
  const feedbackContainer = document.getElementById("feedbackContainer")
  const optionButtons = document.querySelectorAll(".option-btn")

  // Highlight correct and incorrect answers
  optionButtons[correctIndex].classList.add("correct")

  if (selectedIndex !== correctIndex) {
    optionButtons[selectedIndex].classList.add("incorrect")
  }

  // Show feedback message
  const isCorrect = selectedIndex === correctIndex
  feedbackContainer.className = `feedback-container ${isCorrect ? "correct" : "incorrect"}`
  feedbackContainer.innerHTML = `
        <div class="feedback-title">${isCorrect ? "✓ Correct!" : "✗ Incorrect"}</div>
        <div class="feedback-text">${question.explanation}</div>
    `
  feedbackContainer.style.display = "block"
}

// Update navigation buttons
function updateButtons() {
  const prevBtn = document.getElementById("prevBtn")
  const nextBtn = document.getElementById("nextBtn")
  const submitBtn = document.getElementById("submitBtn")

  // Show/hide previous button
  prevBtn.style.display = currentQuestion > 0 ? "inline-block" : "none"

  // Reset buttons for new question
  if (userAnswers[currentQuestion] === null) {
    submitBtn.style.display = "inline-block"
    submitBtn.disabled = true
    nextBtn.style.display = "none"
  } else {
    submitBtn.style.display = "none"
    nextBtn.style.display = "inline-block"
  }

  // Change next button text on last question
  if (currentQuestion === quizData.length - 1) {
    nextBtn.textContent = "View Results"
  } else {
    nextBtn.textContent = "Next Question"
  }
}

// Navigate to previous question
function previousQuestion() {
  if (currentQuestion > 0) {
    currentQuestion--
    displayQuestion()
  }
}

// Navigate to next question
function nextQuestion() {
  if (currentQuestion < quizData.length - 1) {
    currentQuestion++
    displayQuestion()
  } else {
    showResults()
  }
}

// Show results
async function showResults() {
  const score = userAnswers.reduce((total, answer, index) => {
    return total + (answer === quizData[index].correct_answer ? 1 : 0)
  }, 0)

  const percentage = Math.round((score / quizData.length) * 100)
  const incorrect = quizData.length - score

  let grade
  if (percentage >= 90) grade = "A+"
  else if (percentage >= 80) grade = "A"
  else if (percentage >= 70) grade = "B"
  else if (percentage >= 60) grade = "C"
  else if (percentage >= 50) grade = "D"
  else grade = "F"

  // Save score to database
  try {
    await fetch("/api/save-score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: quizTopic,
        score: score,
        total_questions: quizData.length,
      }),
    })
  } catch (error) {
    console.error("Error saving score:", error)
  }

  // Display results
  document.getElementById("quizContent").style.display = "none"
  document.getElementById("resultsContainer").style.display = "block"

  document.getElementById("finalScore").textContent = score
  document.getElementById("totalQuestions").textContent = quizData.length
  document.getElementById("scorePercentage").textContent = `${percentage}%`
  document.getElementById("correctCount").textContent = score
  document.getElementById("incorrectCount").textContent = incorrect
  document.getElementById("grade").textContent = grade

  // Clear session storage
  sessionStorage.removeItem("currentQuiz")
  sessionStorage.removeItem("quizTopic")
}

// Event listeners
document.addEventListener("DOMContentLoaded", () => {
  loadQuiz()

  document.getElementById("prevBtn").addEventListener("click", previousQuestion)
  document.getElementById("nextBtn").addEventListener("click", nextQuestion)
  document.getElementById("submitBtn").addEventListener("click", submitAnswer)
})
