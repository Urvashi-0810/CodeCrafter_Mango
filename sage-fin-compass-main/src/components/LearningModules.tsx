import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Wallet,
  TrendingUp,
  Smartphone,
  Receipt,
  Shield,
  Lock,
  CheckCircle2,
  ChevronRight,
  ArrowLeft,
  Star,
  Zap,
  Heart,
  X,
  Sparkles,
  Trophy,
  Coins
} from "lucide-react"
import {
  LEARNING_MODULES,
  type LearningModule,
  type Lesson,
  type UserProfile,
} from "@/data/learningData"
import { cn } from "@/lib/utils"

const ICON_MAP: Record<string, React.ReactNode> = {
  wallet: <Wallet className="h-6 w-6" />,
  "trending-up": <TrendingUp className="h-6 w-6" />,
  smartphone: <Smartphone className="h-6 w-6" />,
  receipt: <Receipt className="h-6 w-6" />,
  shield: <Shield className="h-6 w-6" />,
}

interface LearningModulesProps {
  profile: UserProfile
  onUpdateProfile: (updates: Partial<UserProfile>) => void
}

export function LearningModules({ profile, onUpdateProfile }: LearningModulesProps) {
  const [modules, setModules] = useState<LearningModule[]>(LEARNING_MODULES)
  const [activeModule, setActiveModule] = useState<LearningModule | null>(null)
  const [activeLesson, setActiveLesson] = useState<Lesson | null>(null)
  const [lives, setLives] = useState(5)

  if (activeLesson && activeModule) {
    return (
      <LessonView
        lesson={activeLesson}
        module={activeModule}
        lives={lives}
        onComplete={(correct) => {
          if (!correct) {
            setLives((l) => Math.max(0, l - 1))
          }
          // Mark lesson complete
          setModules((prev) =>
            prev.map((m) =>
              m.id === activeModule.id
                ? {
                    ...m,
                    lessons: m.lessons.map((l) =>
                      l.id === activeLesson.id ? { ...l, completed: true } : l
                    ),
                    progress:
                      ((m.lessons.filter((l) => l.completed || l.id === activeLesson.id)
                        .length) /
                        m.lessons.length) *
                      100,
                  }
                : m
            )
          )
          const xpGain = correct ? activeLesson.xpReward : Math.floor(activeLesson.xpReward / 2)
          const newXp = profile.xp + xpGain
          const newCoins = profile.totalCoins + (correct ? 15 : 5)
          const newLevel = Math.floor(newXp / 100) + 1
          onUpdateProfile({
            xp: newXp,
            level: newLevel,
            totalCoins: newCoins,
            xpToNext: (newLevel) * 100,
          })
          setActiveLesson(null)
        }}
        onBack={() => setActiveLesson(null)}
      />
    )
  }

  if (activeModule) {
    return (
      <ModuleView
        profile={profile}
        module={modules.find((m) => m.id === activeModule.id) || activeModule}
        lives={lives}
        onSelectLesson={(lesson) => setActiveLesson(lesson)}
        onBack={() => setActiveModule(null)}
      />
    )
  }

  return (
    <div className="px-4 py-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-extrabold text-foreground">Learn</h1>
          <p className="text-sm text-muted-foreground">Master finance, one lesson at a time</p>
        </div>
        <div className="flex items-center gap-1 rounded-full bg-rose-500/10 px-3 py-1">
          <Heart className="h-4 w-4 fill-rose-500 text-rose-500" />
          <span className="text-sm font-bold text-rose-500">{lives}</span>
        </div>
      </div>

      {/* Gamification Stats (Added directly into UI instead of Navbar) */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <Card className="border-2 border-primary/20 bg-primary/5 shadow-sm">
          <CardContent className="p-3 text-center flex flex-col items-center justify-center">
            <Trophy className="h-5 w-5 text-amber-500 mb-1" />
            <span className="text-xs font-bold text-muted-foreground">Level {profile.level}</span>
            <span className="text-sm font-extrabold text-amber-600">{profile.xp} XP</span>
          </CardContent>
        </Card>
        <Card className="border-2 border-primary/20 bg-primary/5 shadow-sm">
          <CardContent className="p-3 text-center flex flex-col items-center justify-center">
            <Coins className="h-5 w-5 text-amber-400 mb-1" />
            <span className="text-xs font-bold text-muted-foreground">Wealth</span>
            <span className="text-sm font-extrabold text-amber-500">{profile.totalCoins}</span>
          </CardContent>
        </Card>
        <Card className="border-2 border-primary/20 bg-primary/5 shadow-sm">
          <CardContent className="p-3 text-center flex flex-col items-center justify-center">
            <Zap className="h-5 w-5 text-indigo-500 mb-1" />
            <span className="text-xs font-bold text-muted-foreground">Streak</span>
            <span className="text-sm font-extrabold text-indigo-600">{profile.streak} Days</span>
          </CardContent>
        </Card>
      </div>

      {/* Module Path - Duolingo Style */}
      <div className="relative">
        {/* Connecting Line */}
        <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-border" />

        <div className="space-y-4">
          {modules.map((module, index) => {
            const completedLessons = module.lessons.filter((l) => l.completed).length
            const isComplete = completedLessons === module.lessons.length && module.lessons.length > 0
            const isLocked = module.locked && index > 0 && modules[index - 1].progress < 100

            return (
              <div key={module.id} className="relative flex items-center gap-4">
                {/* Node */}
                <div
                  className={cn(
                    "relative z-10 flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 transition-all",
                    isComplete
                      ? "border-primary bg-primary text-primary-foreground shadow-lg shadow-primary/20"
                      : isLocked
                      ? "border-border bg-muted text-muted-foreground"
                      : "border-primary/50 bg-card text-primary hover:scale-105"
                  )}
                >
                  {isLocked ? (
                    <Lock className="h-6 w-6" />
                  ) : isComplete ? (
                    <CheckCircle2 className="h-7 w-7" />
                  ) : (
                    ICON_MAP[module.icon] || <Star className="h-6 w-6" />
                  )}
                </div>

                {/* Card */}
                <Card
                  className={cn(
                    "flex-1 cursor-pointer transition-all",
                    isLocked
                      ? "opacity-50"
                      : "hover:shadow-md active:scale-[0.99]"
                  )}
                  onClick={() => !isLocked && setActiveModule(module)}
                >
                  <CardContent className="flex items-center gap-3 p-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-bold text-foreground text-sm">
                          {module.title}
                        </p>
                        {isComplete && (
                          <Badge className="bg-primary/10 text-primary text-[10px]">
                            Complete
                          </Badge>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {module.description}
                      </p>
                      <div className="mt-2 flex items-center gap-2">
                        <Progress
                          value={module.progress}
                          className="h-1.5 flex-1"
                        />
                        <span className="text-[10px] font-bold text-muted-foreground">
                          {completedLessons}/{module.lessons.length}
                        </span>
                      </div>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground" />
                  </CardContent>
                </Card>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

function ModuleView({
  profile,
  module,
  lives,
  onSelectLesson,
  onBack,
}: {
  profile: UserProfile
  module: LearningModule
  lives: number
  onSelectLesson: (lesson: Lesson) => void
  onBack: () => void
}) {
  return (
    <div className="px-4 py-6">
      {/* Header */}
      <div className="mb-6 flex items-center gap-3">
        <Button variant="ghost" size="icon" onClick={onBack}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div className="flex-1">
          <h2 className="text-lg font-extrabold text-foreground">{module.title}</h2>
          <p className="text-xs text-muted-foreground">{module.description}</p>
        </div>
        <div className="flex items-center gap-1">
          <Heart className="h-4 w-4 fill-rose-500 text-rose-500" />
          <span className="text-sm font-bold text-rose-500">{lives}</span>
        </div>
      </div>

      {/* Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
          <span>Progress</span>
          <span>{Math.round(module.progress)}%</span>
        </div>
        <Progress value={module.progress} className="h-2" />
        
        {/* Gamification Level Below Module Progress */}
        <div className="mt-3 flex items-center justify-between bg-primary/5 border border-primary/20 rounded-lg p-3 shadow-sm">
          <div className="flex items-center gap-2">
            <Trophy className="h-4 w-4 text-amber-500" />
            <span className="text-xs font-bold text-muted-foreground">Level {profile.level}</span>
          </div>
          <div className="text-right">
            <span className="text-xs font-extrabold text-amber-600">{profile.xp} / {profile.xpToNext} XP</span>
          </div>
        </div>
      </div>

      {/* Lessons List */}
      <div className="space-y-3">
        {module.lessons.map((lesson, index) => {
          const isLocked = index > 0 && !module.lessons[index - 1].completed
          return (
            <Card
              key={lesson.id}
              className={cn(
                "cursor-pointer transition-all",
                lesson.completed && "border-primary/30 bg-primary/5",
                isLocked && "opacity-50"
              )}
              onClick={() => !isLocked && onSelectLesson(lesson)}
            >
              <CardContent className="flex items-center gap-4 p-4">
                <div
                  className={cn(
                    "flex h-10 w-10 shrink-0 items-center justify-center rounded-xl",
                    lesson.completed
                      ? "bg-primary text-primary-foreground"
                      : isLocked
                      ? "bg-muted text-muted-foreground"
                      : "bg-primary/10 text-primary"
                  )}
                >
                  {lesson.completed ? (
                    <CheckCircle2 className="h-5 w-5" />
                  ) : isLocked ? (
                    <Lock className="h-5 w-5" />
                  ) : (
                    <span className="text-sm font-extrabold">{index + 1}</span>
                  )}
                </div>
                <div className="flex-1">
                  <p className="font-bold text-foreground text-sm">{lesson.title}</p>
                  <div className="mt-0.5 flex items-center gap-2">
                    <Badge variant="secondary" className="text-[10px]">
                      {lesson.type === "info"
                        ? "Lesson"
                        : lesson.type === "quiz"
                        ? "Quiz"
                        : lesson.type === "match"
                        ? "Match"
                        : "Fill"}
                    </Badge>
                    <span className="flex items-center gap-0.5 text-[10px] font-semibold text-accent">
                      <Star className="h-3 w-3" />+{lesson.xpReward} XP
                    </span>
                  </div>
                </div>
                <ChevronRight className="h-4 w-4 text-muted-foreground" />
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

function LessonView({
  lesson,
  module,
  lives,
  onComplete,
  onBack,
}: {
  lesson: Lesson
  module: LearningModule
  lives: number
  onComplete: (correct: boolean) => void
  onBack: () => void
}) {
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [matchedPairs, setMatchedPairs] = useState<Set<number>>(new Set())
  const [selectedLeft, setSelectedLeft] = useState<number | null>(null)

  if (lesson.type === "info") {
    return (
      <div className="flex min-h-[calc(100dvh-8rem)] flex-col px-4 py-6">
        <div className="mb-6 flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <X className="h-5 w-5" />
          </Button>
          <Progress value={50} className="flex-1 h-2" />
          <div className="flex items-center gap-1">
            <Heart className="h-4 w-4 fill-rose-500 text-rose-500" />
            <span className="text-sm font-bold text-rose-500">{lives}</span>
          </div>
        </div>

        <div className="flex-1 bg-background">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
            <Sparkles className="h-7 w-7 text-primary" />
          </div>
          <h2 className="text-xl font-extrabold text-foreground mb-4">
            {lesson.title}
          </h2>
          <Card className="border-2 shadow-sm">
            <CardContent className="p-5">
              <p className="text-sm text-foreground leading-relaxed">
                {lesson.content}
              </p>
            </CardContent>
          </Card>
        </div>

        <Button
          className="mt-6 w-full"
          size="lg"
          onClick={() => onComplete(true)}
        >
          Continue
          <ChevronRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    )
  }

  if (lesson.type === "quiz") {
    const isCorrect = selectedAnswer === lesson.correctAnswer

    return (
      <div className="flex min-h-[calc(100dvh-8rem)] flex-col px-4 py-6">
        <div className="mb-6 flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <X className="h-5 w-5" />
          </Button>
          <Progress value={75} className="flex-1 h-2" />
          <div className="flex items-center gap-1">
            <Heart className="h-4 w-4 fill-rose-500 text-rose-500" />
            <span className="text-sm font-bold text-rose-500">{lives}</span>
          </div>
        </div>

        <div className="flex-1">
          <p className="text-xs font-bold uppercase tracking-wider text-primary mb-2">
            Select the correct answer
          </p>
          <h2 className="text-lg font-extrabold text-foreground mb-6 leading-relaxed">
            {lesson.question}
          </h2>

          <div className="space-y-3">
            {lesson.options?.map((option, index) => (
              <button
                key={index}
                disabled={showResult}
                onClick={() => setSelectedAnswer(index)}
                className={cn(
                  "w-full rounded-xl border-2 p-4 text-left text-sm font-semibold transition-all",
                  selectedAnswer === index && !showResult
                    ? "border-primary bg-primary/5 text-primary"
                    : "border-border text-foreground hover:border-primary/50",
                  showResult &&
                    index === lesson.correctAnswer &&
                    "border-emerald-500 bg-emerald-500/10 text-emerald-600",
                  showResult &&
                    selectedAnswer === index &&
                    index !== lesson.correctAnswer &&
                    "border-rose-500 bg-rose-500/10 text-rose-600"
                )}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border-2 text-xs font-extrabold",
                      selectedAnswer === index && !showResult
                        ? "border-primary bg-primary text-primary-foreground"
                        : "border-border",
                      showResult &&
                        index === lesson.correctAnswer &&
                        "border-emerald-500 bg-emerald-500 text-white",
                      showResult &&
                        selectedAnswer === index &&
                        index !== lesson.correctAnswer &&
                        "border-rose-500 bg-rose-500 text-white"
                    )}
                  >
                    {String.fromCharCode(65 + index)}
                  </div>
                  {option}
                </div>
              </button>
            ))}
          </div>
        </div>

        {!showResult ? (
          <Button
            className="mt-6 w-full"
            size="lg"
            disabled={selectedAnswer === null}
            onClick={() => setShowResult(true)}
          >
            Check Answer
          </Button>
        ) : (
          <div className="mt-6">
            <Card
              className={cn(
                "mb-3 border-2 shadow-sm",
                isCorrect
                  ? "border-emerald-500/30 bg-emerald-500/5"
                  : "border-rose-500/30 bg-rose-500/5"
              )}
            >
              <CardContent className="p-4">
                <p
                  className={cn(
                    "font-extrabold",
                    isCorrect ? "text-emerald-600" : "text-rose-600"
                  )}
                >
                  {isCorrect ? "Correct!" : "Not quite!"}
                </p>
                <p className="mt-1 text-xs text-muted-foreground">
                  {isCorrect
                    ? `+${lesson.xpReward} XP earned!`
                    : `The correct answer was: ${lesson.options?.[lesson.correctAnswer || 0]}`}
                </p>
              </CardContent>
            </Card>
            <Button
              className="w-full"
              size="lg"
              onClick={() => onComplete(isCorrect)}
            >
              Continue
            </Button>
          </div>
        )}
      </div>
    )
  }

  // Match type
  if (lesson.type === "match" && lesson.pairs) {
    const allMatched = matchedPairs.size === lesson.pairs.length

    return (
      <div className="flex min-h-[calc(100dvh-8rem)] flex-col px-4 py-6">
        <div className="mb-6 flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <X className="h-5 w-5" />
          </Button>
          <Progress value={60} className="flex-1 h-2" />
          <div className="flex items-center gap-1">
            <Heart className="h-4 w-4 fill-rose-500 text-rose-500" />
            <span className="text-sm font-bold text-rose-500">{lives}</span>
          </div>
        </div>

        <div className="flex-1">
          <p className="text-xs font-bold uppercase tracking-wider text-primary mb-2">
            Match the pairs
          </p>
          <h2 className="text-lg font-extrabold text-foreground mb-6">
            {lesson.title}
          </h2>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              {lesson.pairs.map((pair, index) => (
                <button
                  key={`left-${index}`}
                  disabled={matchedPairs.has(index)}
                  onClick={() => setSelectedLeft(index)}
                  className={cn(
                    "w-full rounded-xl border-2 p-3 text-sm font-semibold transition-all",
                    matchedPairs.has(index)
                      ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 opacity-60"
                      : selectedLeft === index
                      ? "border-primary bg-primary/5 text-primary"
                      : "border-border text-foreground"
                  )}
                >
                  {pair.left}
                </button>
              ))}
            </div>
            <div className="space-y-2">
               {lesson.pairs.map((pair, index) => (
                <button
                  key={`right-${index}`}
                  disabled={matchedPairs.has(index)}
                  onClick={() => {
                    if (selectedLeft !== null && selectedLeft === index) {
                      setMatchedPairs((prev) => new Set([...prev, index]))
                      setSelectedLeft(null)
                    } else {
                      setSelectedLeft(null)
                    }
                  }}
                  className={cn(
                    "w-full rounded-xl border-2 p-3 text-sm font-semibold transition-all",
                    matchedPairs.has(index)
                      ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 opacity-60"
                      : "border-border text-foreground hover:border-primary/50"
                  )}
                >
                  {pair.right}
                </button>
              ))}
            </div>
          </div>
        </div>

        {allMatched && (
          <div className="mt-6">
            <Card className="mb-3 border-2 border-emerald-500/30 bg-emerald-500/5 shadow-sm">
              <CardContent className="p-4 text-center">
                <p className="font-extrabold text-emerald-600">
                  All matched! +{lesson.xpReward} XP
                </p>
              </CardContent>
            </Card>
            <Button
              className="w-full"
              size="lg"
              onClick={() => onComplete(true)}
            >
              Continue
            </Button>
          </div>
        )}
      </div>
    )
  }

  return null
}
