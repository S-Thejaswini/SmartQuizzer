"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { QuizCard } from "@/components/quiz-card"
import { ScoreDisplay } from "@/components/score-display"
import { quizTopics, type QuizTopic } from "@/lib/quiz-data"
import { BookOpen, ArrowRight } from "lucide-react"

type GameState = "topic-selection" | "quiz" | "results"

export default function Home() {
  const [gameState, setGameState] = useState<GameState>("topic-selection")
  const [selectedTopic, setSelectedTopic] = useState<QuizTopic | null>(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [answers, setAnswers] = useState<boolean[]>([])

  const handleTopicSelect = (topic: QuizTopic) => {
    setSelectedTopic(topic)
    setGameState("quiz")
    setCurrentQuestionIndex(0)
    setScore(0)
    setAnswers([])
  }

  const handleAnswer = (isCorrect: boolean) => {
    if (answers[currentQuestionIndex] === undefined) {
      const newAnswers = [...answers]
      newAnswers[currentQuestionIndex] = isCorrect
      setAnswers(newAnswers)
      if (isCorrect) {
        setScore(score + 1)
      }
    }
  }

  const handleNext = () => {
    if (selectedTopic && currentQuestionIndex < selectedTopic.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      setGameState("results")
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const handleRestart = () => {
    setCurrentQuestionIndex(0)
    setScore(0)
    setAnswers([])
    setGameState("quiz")
  }

  const handleBackToTopics = () => {
    setGameState("topic-selection")
    setSelectedTopic(null)
    setCurrentQuestionIndex(0)
    setScore(0)
    setAnswers([])
  }

  if (gameState === "topic-selection") {
    return (
      <main className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-4 md:p-8">
        <div className="max-w-6xl mx-auto space-y-8">
          <div className="text-center space-y-4 py-8">
            <div className="flex justify-center mb-4">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center">
                <BookOpen className="w-8 h-8 text-primary" />
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-balance">SmartQuizzer</h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-balance">
              Test your knowledge across multiple topics. Choose a quiz below to get started!
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {quizTopics.map((topic) => (
              <Card
                key={topic.id}
                className="group hover:shadow-lg transition-all duration-200 hover:scale-[1.02] cursor-pointer"
                onClick={() => handleTopicSelect(topic)}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="text-4xl mb-2">{topic.icon}</div>
                    <Badge variant="secondary">{topic.questions.length} questions</Badge>
                  </div>
                  <CardTitle className="text-xl">{topic.title}</CardTitle>
                  <CardDescription className="text-pretty">{topic.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full gap-2 group-hover:gap-3 transition-all">
                    Start Quiz
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </main>
    )
  }

  if (gameState === "quiz" && selectedTopic) {
    const currentQuestion = selectedTopic.questions[currentQuestionIndex]
    return (
      <main className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-4 md:p-8">
        <div className="max-w-4xl mx-auto space-y-8 py-8">
          <div className="text-center space-y-2">
            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <span className="text-2xl">{selectedTopic.icon}</span>
              <span>{selectedTopic.title}</span>
            </div>
          </div>

          <QuizCard
            question={currentQuestion}
            questionNumber={currentQuestionIndex + 1}
            totalQuestions={selectedTopic.questions.length}
            onAnswer={handleAnswer}
            onNext={handleNext}
            onPrevious={handlePrevious}
            isFirst={currentQuestionIndex === 0}
            isLast={currentQuestionIndex === selectedTopic.questions.length - 1}
          />
        </div>
      </main>
    )
  }

  if (gameState === "results" && selectedTopic) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-4 md:p-8">
        <div className="max-w-4xl mx-auto space-y-8 py-8">
          <ScoreDisplay
            score={score}
            totalQuestions={selectedTopic.questions.length}
            onRestart={handleRestart}
            onBackToTopics={handleBackToTopics}
          />
        </div>
      </main>
    )
  }

  return null
}
