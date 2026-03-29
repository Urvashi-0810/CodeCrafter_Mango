export interface LearningModule {
  id: string
  title: string
  description: string
  icon: string
  lessons: Lesson[]
  color: string
  progress: number
  locked: boolean
}

export interface Lesson {
  id: string
  title: string
  type: "info" | "quiz" | "match" | "fill"
  completed: boolean
  xpReward: number
  content?: string
  question?: string
  options?: string[]
  correctAnswer?: number
  pairs?: { left: string; right: string }[]
}

export interface UserProfile {
  name: string
  level: number
  xp: number
  xpToNext: number
  streak: number
  totalCoins: number
  virtualBalance: number
  badges: Badge[]
  portfolioHealth: number
}

export interface Badge {
  id: string
  name: string
  icon: string
  description: string
  earned: boolean
}

export const LEARNING_MODULES: LearningModule[] = [
  {
    id: "budgeting",
    title: "Budgeting Basics",
    description: "Master the art of managing your money",
    icon: "wallet",
    color: "bg-emerald-500",
    progress: 0,
    locked: false,
    lessons: [
      { id: "b1", title: "What is a Budget?", type: "info", completed: false, xpReward: 10, content: "A budget is a plan for your money. It helps you track where your money comes from and where it goes. The 50/30/20 rule suggests spending 50% on needs, 30% on wants, and 20% on savings." },
      { id: "b2", title: "50/30/20 Rule Quiz", type: "quiz", completed: false, xpReward: 20, question: "According to the 50/30/20 rule, what percentage should go to savings?", options: ["10%", "20%", "30%", "50%"], correctAnswer: 1 },
      { id: "b3", title: "Match the Category", type: "match", completed: false, xpReward: 25, pairs: [{ left: "Rent", right: "Need" }, { left: "Netflix", right: "Want" }, { left: "SIP", right: "Savings" }, { left: "Groceries", right: "Need" }] },
      { id: "b4", title: "Income vs Expenses", type: "info", completed: false, xpReward: 10, content: "Your income is the money you earn. Expenses are what you spend. The goal is to always have income > expenses. Track every rupee to find leaks in your budget!" },
      { id: "b5", title: "Budget Check", type: "quiz", completed: false, xpReward: 20, question: "Riya earns Rs 30,000/month. She spends Rs 15,000 on needs, Rs 10,000 on wants. How much is left for savings?", options: ["Rs 3,000", "Rs 5,000", "Rs 7,000", "Rs 10,000"], correctAnswer: 1 },
    ]
  },
  {
    id: "sip",
    title: "Power of SIP",
    description: "Learn how small investments grow big",
    icon: "trending-up",
    color: "bg-blue-500",
    progress: 0,
    locked: false,
    lessons: [
      { id: "s1", title: "What is SIP?", type: "info", completed: false, xpReward: 10, content: "SIP (Systematic Investment Plan) lets you invest a fixed amount regularly in mutual funds. Even Rs 500/month can grow into lakhs over time thanks to compounding!" },
      { id: "s2", title: "Compounding Magic", type: "quiz", completed: false, xpReward: 20, question: "Rs 5,000/month SIP for 20 years at 12% return becomes approximately?", options: ["Rs 12 Lakhs", "Rs 25 Lakhs", "Rs 50 Lakhs", "Rs 75 Lakhs"], correctAnswer: 2 },
      { id: "s3", title: "SIP vs Lump Sum", type: "info", completed: false, xpReward: 15, content: "SIP averages out the cost through rupee cost averaging. When markets are down, you buy more units. When up, fewer units. This reduces risk compared to investing everything at once." },
      { id: "s4", title: "Test Your Knowledge", type: "quiz", completed: false, xpReward: 25, question: "What is the key benefit of SIP in a volatile market?", options: ["Guaranteed returns", "Rupee cost averaging", "Zero risk", "Tax free returns"], correctAnswer: 1 },
    ]
  },
  {
    id: "upi",
    title: "UPI & Digital Payments",
    description: "Stay safe in the digital payment world",
    icon: "smartphone",
    color: "bg-orange-500",
    progress: 0,
    locked: false,
    lessons: [
      { id: "u1", title: "How UPI Works", type: "info", completed: false, xpReward: 10, content: "UPI (Unified Payments Interface) links your bank account to a virtual address. You can send/receive money instantly. Popular apps: PhonePe, GPay, Paytm. Always verify before sending!" },
      { id: "u2", title: "UPI Safety Quiz", type: "quiz", completed: false, xpReward: 20, question: "When does someone need YOUR UPI PIN?", options: ["To send you money", "To receive your money", "Never - only YOU use your PIN", "To verify your account"], correctAnswer: 2 },
      { id: "u3", title: "Spot the Scam", type: "quiz", completed: false, xpReward: 25, question: "Someone asks you to scan a QR code to RECEIVE money. What should you do?", options: ["Scan it quickly", "Ask for a different QR code", "Refuse - QR codes are for SENDING money", "Share your OTP too"], correctAnswer: 2 },
    ]
  },
  {
    id: "tax",
    title: "Tax Basics",
    description: "Decode Indian income tax easily",
    icon: "receipt",
    color: "bg-rose-500",
    progress: 0,
    locked: true,
    lessons: [
      { id: "t1", title: "Income Tax Slabs", type: "info", completed: false, xpReward: 10, content: "India has a new tax regime: Up to 3L = 0%, 3-7L = 5%, 7-10L = 10%, 10-12L = 15%, 12-15L = 20%, Above 15L = 30%. The old regime has deductions like 80C." },
      { id: "t2", title: "Tax Slab Quiz", type: "quiz", completed: false, xpReward: 20, question: "Under the new regime, income up to Rs 3 Lakh is taxed at?", options: ["5%", "10%", "0%", "15%"], correctAnswer: 2 },
      { id: "t3", title: "Section 80C", type: "info", completed: false, xpReward: 15, content: "Section 80C allows deductions up to Rs 1.5 Lakh from taxable income. Eligible investments: ELSS, PPF, EPF, life insurance, tuition fees, NSC, and more." },
    ]
  },
  {
    id: "credit",
    title: "Credit Score Mastery",
    description: "Build and maintain a great CIBIL score",
    icon: "shield",
    color: "bg-indigo-500",
    progress: 0,
    locked: true,
    lessons: [
      { id: "c1", title: "What is CIBIL Score?", type: "info", completed: false, xpReward: 10, content: "CIBIL score ranges from 300-900. A score above 750 is considered good. It affects your ability to get loans and credit cards. Factors: payment history (35%), credit utilization (30%), credit age (15%), credit mix (10%), inquiries (10%)." },
      { id: "c2", title: "Score Factors Quiz", type: "quiz", completed: false, xpReward: 20, question: "Which factor has the HIGHEST impact on your CIBIL score?", options: ["Credit mix", "Payment history", "Number of inquiries", "Credit age"], correctAnswer: 1 },
    ]
  },
]

export const INITIAL_PROFILE: UserProfile = {
  name: "Smart Investor",
  level: 1,
  xp: 0,
  xpToNext: 100,
  streak: 3,
  totalCoins: 500,
  virtualBalance: 1000000,
  badges: [
    { id: "first-step", name: "First Step", icon: "footprints", description: "Started your financial journey", earned: true },
    { id: "investor", name: "Rookie Investor", icon: "bar-chart", description: "Made your first investment", earned: false },
    { id: "scholar", name: "Finance Scholar", icon: "graduation-cap", description: "Completed all learning modules", earned: false },
    { id: "streak7", name: "Weekly Warrior", icon: "flame", description: "Maintained a 7-day streak", earned: false },
  ],
  portfolioHealth: 72,
}
