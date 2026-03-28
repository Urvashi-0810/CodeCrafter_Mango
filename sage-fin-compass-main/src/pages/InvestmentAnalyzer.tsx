import { useState } from "react";
import {
  PieChart as PieChartIcon, Sparkles, ChevronRight, TrendingUp, AlertCircle,
  ArrowUpRight, Shield, RefreshCw
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

interface InvestmentEntry {
  type: string;
  amount: number;
  details: string;
}

const investmentTypes = [
  "Equity / Stocks",
  "Mutual Funds",
  "Gold",
  "Fixed Deposits",
  "Bonds / Debentures",
  "Real Estate",
  "PPF / EPF",
  "NPS",
  "Crypto",
  "Others",
];

const aiStrategies = [
  {
    type: "diversification",
    title: "Rebalance: Reduce Equity, Add Gold & Bonds",
    detail: "Your 55% equity allocation exceeds the recommended 40-45% for moderate risk. Shift 10% to Gold ETFs (currently at 5%) and 5% to Government Bonds for better downside protection. Given current market volatility (VIX at 16.5), a more balanced allocation would limit maximum drawdown to ~12% vs current exposure of ~18%.",
    risk: "Medium",
  },
  {
    type: "growth",
    title: "Increase SIP in Flexi-Cap Mutual Funds",
    detail: "Based on your risk tolerance, increase monthly SIP by ₹5,000 in a flexi-cap fund. Historical data shows flexi-cap funds delivered 15.2% CAGR over 10 years vs 12.8% for large-cap funds. This allows fund managers to capture mid-cap growth while maintaining large-cap stability.",
    risk: "Medium",
  },
  {
    type: "protection",
    title: "Hedge with Put Options During Earnings Season",
    detail: "Your concentrated equity portfolio is vulnerable during Q4 earnings season (April-May). Consider buying NIFTY put options with 5% OTM strike for portfolio insurance. Cost: ~0.5% of portfolio value for 30-day protection. This caps your maximum loss at 5% regardless of market movement.",
    risk: "Low",
  },
  {
    type: "opportunity",
    title: "Debt Fund Opportunity: Short-Duration Funds",
    detail: "With RBI expected to cut rates by 25-50bps in the next 6 months, short-duration debt funds could yield 7.5-8.5% returns. Allocate 15% of your FD corpus to short-duration funds for better tax efficiency (LTCG after 2 years) and higher post-tax returns compared to FDs.",
    risk: "Low",
  },
  {
    type: "sector",
    title: "Sector Rotation: Move from FMCG to Defense",
    detail: "FMCG sector is trading at historically high valuations (PE: 45x) with slowing volume growth. India's defense budget grew 13% YoY to ₹6.2L crore. Consider rotating 5% from FMCG to defense stocks (HAL, BEL, BDL) which trade at reasonable valuations with strong order book visibility of 3-4 years.",
    risk: "Medium-High",
  },
];

export default function InvestmentAnalyzer() {
  const [step, setStep] = useState<"form" | "analysis">("form");
  const [investments, setInvestments] = useState<InvestmentEntry[]>([
    { type: "Equity / Stocks", amount: 500000, details: "Large-cap focused, 8 stocks across IT, Banking, FMCG" },
    { type: "Mutual Funds", amount: 300000, details: "3 SIPs: Flexi-cap, Mid-cap, ELSS. Monthly: ₹15,000 total" },
    { type: "Gold", amount: 100000, details: "Sovereign Gold Bonds + Gold ETF" },
    { type: "Fixed Deposits", amount: 200000, details: "SBI FD at 7.1% p.a., maturing Dec 2025" },
    { type: "PPF / EPF", amount: 150000, details: "PPF: ₹1.5L annual. EPF: employer match" },
  ]);
  const [riskTolerance, setRiskTolerance] = useState("moderate");
  const [returnTarget, setReturnTarget] = useState("12");
  const [addType, setAddType] = useState("");
  const [addAmount, setAddAmount] = useState("");
  const [addDetails, setAddDetails] = useState("");

  const totalInvestment = investments.reduce((sum, inv) => sum + inv.amount, 0);

  const chartData = investments.map((inv) => ({
    name: inv.type,
    value: +((inv.amount / totalInvestment) * 100).toFixed(1),
  }));

  const colors = ["hsl(160,84%,39%)", "hsl(217,91%,60%)", "hsl(38,92%,50%)", "hsl(270,76%,55%)", "hsl(0,72%,51%)", "hsl(160,60%,50%)", "hsl(200,80%,50%)", "hsl(330,70%,50%)"];

  const barData = investments.map((inv) => ({
    name: inv.type.split(" ")[0],
    amount: inv.amount / 1000,
  }));

  const handleAdd = () => {
    if (!addType || !addAmount) return;
    setInvestments([...investments, { type: addType, amount: parseFloat(addAmount), details: addDetails }]);
    setAddType("");
    setAddAmount("");
    setAddDetails("");
  };

  const removeInvestment = (index: number) => {
    setInvestments(investments.filter((_, i) => i !== index));
  };

  if (step === "analysis") {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <TickerBar />
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
                <PieChartIcon className="h-8 w-8 text-primary" /> Investment Analysis
              </h1>
              <p className="mt-1 text-muted-foreground">AI-powered strategies based on your {riskTolerance} risk profile</p>
            </div>
            <Button variant="outline" onClick={() => setStep("form")} className="gap-1">
              <RefreshCw className="h-3.5 w-3.5" /> Modify Inputs
            </Button>
          </div>

          {/* Summary */}
          <div className="grid gap-4 sm:grid-cols-4 mb-6">
            <div className="glass-card p-4">
              <span className="text-xs text-muted-foreground">Total Investment</span>
              <div className="font-heading text-xl font-bold text-primary mt-1">₹{(totalInvestment / 100000).toFixed(1)}L</div>
            </div>
            <div className="glass-card p-4">
              <span className="text-xs text-muted-foreground">Asset Classes</span>
              <div className="font-heading text-xl font-bold mt-1">{investments.length}</div>
            </div>
            <div className="glass-card p-4">
              <span className="text-xs text-muted-foreground">Risk Profile</span>
              <div className="font-heading text-xl font-bold mt-1 capitalize">{riskTolerance}</div>
            </div>
            <div className="glass-card p-4">
              <span className="text-xs text-muted-foreground">Target Return</span>
              <div className="font-heading text-xl font-bold text-primary mt-1">{returnTarget}% p.a.</div>
            </div>
          </div>

          {/* Charts */}
          <div className="grid gap-6 md:grid-cols-2 mb-8">
            <div className="glass-card p-5">
              <h3 className="font-heading text-base font-semibold mb-3">Current Allocation</h3>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} innerRadius={55} strokeWidth={0}>
                    {chartData.map((_, i) => (
                      <Cell key={i} fill={colors[i % colors.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ background: "hsl(222,47%,9%)", border: "1px solid hsl(217,33%,17%)", borderRadius: 8, fontSize: 12, color: "#fff" }}
                    itemStyle={{ color: "#fff" }}
                    formatter={(v: number) => [`${v}%`, "Allocation"]}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="grid grid-cols-2 gap-1 mt-2">
                {chartData.map((s, i) => (
                  <div key={s.name} className="flex items-center gap-2 text-xs">
                    <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ background: colors[i % colors.length] }} />
                    <span className="truncate">{s.name}</span>
                    <span className="font-medium ml-auto">{s.value}%</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="glass-card p-5">
              <h3 className="font-heading text-base font-semibold mb-3">Investment Breakdown (₹K)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={barData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(217,33%,17%)" />
                  <XAxis type="number" tick={{ fontSize: 10, fill: "hsl(215,20%,55%)" }} />
                  <YAxis dataKey="name" type="category" width={60} tick={{ fontSize: 10, fill: "hsl(215,20%,55%)" }} />
                  <Tooltip
                    contentStyle={{ background: "hsl(222,47%,9%)", border: "1px solid hsl(217,33%,17%)", borderRadius: 8, fontSize: 12, color: "#fff" }}
                    itemStyle={{ color: "#fff" }}
                    formatter={(v: number) => [`₹${v}K`, "Amount"]}
                  />
                  <Bar dataKey="amount" fill="hsl(160,84%,39%)" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* AI Strategies */}
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="h-5 w-5 text-primary" />
            <h2 className="font-heading text-lg font-semibold">AI Investment Strategies</h2>
          </div>
          <div className="space-y-4">
            {aiStrategies.map((strategy, i) => (
              <div
                key={i}
                className={`glass-card p-5 border-l-4 ${
                  strategy.type === "diversification" ? "border-l-chart-amber" :
                  strategy.type === "growth" ? "border-l-primary" :
                  strategy.type === "protection" ? "border-l-chart-blue" :
                  strategy.type === "opportunity" ? "border-l-chart-purple" :
                  "border-l-warning"
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  {strategy.type === "diversification" && <PieChartIcon className="h-4 w-4 text-chart-amber" />}
                  {strategy.type === "growth" && <TrendingUp className="h-4 w-4 text-primary" />}
                  {strategy.type === "protection" && <Shield className="h-4 w-4 text-chart-blue" />}
                  {strategy.type === "opportunity" && <ArrowUpRight className="h-4 w-4 text-chart-purple" />}
                  {strategy.type === "sector" && <AlertCircle className="h-4 w-4 text-warning" />}
                  <h3 className="font-heading text-sm font-semibold">{strategy.title}</h3>
                  <Badge variant="outline" className="text-[10px] ml-auto">Risk: {strategy.risk}</Badge>
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">{strategy.detail}</p>
              </div>
            ))}
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <TickerBar />

      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="mb-8">
          <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
            <PieChartIcon className="h-8 w-8 text-primary" /> Investment Analyzer
          </h1>
          <p className="mt-1 text-muted-foreground">
            Input your investments across sectors for AI-powered diversification strategies
          </p>
        </div>

        {/* Current Investments */}
        <div className="glass-card p-5 mb-6">
          <h2 className="font-heading text-base font-semibold mb-4">Your Investments</h2>
          <div className="space-y-3">
            {investments.map((inv, i) => (
              <div key={i} className="flex items-center gap-3 rounded-lg border border-border/30 bg-background/50 p-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-xs">{inv.type}</Badge>
                    <span className="font-heading text-sm font-bold">₹{inv.amount.toLocaleString()}</span>
                  </div>
                  {inv.details && <p className="text-xs text-muted-foreground mt-1">{inv.details}</p>}
                </div>
                <Button variant="ghost" size="sm" className="text-xs text-muted-foreground hover:text-destructive" onClick={() => removeInvestment(i)}>
                  Remove
                </Button>
              </div>
            ))}
          </div>

          {/* Add Investment */}
          <div className="mt-4 border-t border-border/50 pt-4">
            <h3 className="text-sm font-medium mb-3">Add Investment</h3>
            <div className="grid gap-3 sm:grid-cols-3">
              <Select value={addType} onValueChange={setAddType}>
                <SelectTrigger className="bg-background">
                  <SelectValue placeholder="Investment Type" />
                </SelectTrigger>
                <SelectContent>
                  {investmentTypes.map((t) => (
                    <SelectItem key={t} value={t}>{t}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Input
                type="number"
                placeholder="Amount (₹)"
                value={addAmount}
                onChange={(e) => setAddAmount(e.target.value)}
                className="bg-background"
              />
              <Input
                placeholder="Details (optional)"
                value={addDetails}
                onChange={(e) => setAddDetails(e.target.value)}
                className="bg-background"
              />
            </div>
            <Button size="sm" className="mt-3" onClick={handleAdd}>Add Investment</Button>
          </div>
        </div>

        {/* Risk & Return Preferences */}
        <div className="glass-card p-5 mb-6">
          <h2 className="font-heading text-base font-semibold mb-4">Your Preferences</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Risk Tolerance</label>
              <Select value={riskTolerance} onValueChange={setRiskTolerance}>
                <SelectTrigger className="bg-background">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="conservative">Conservative</SelectItem>
                  <SelectItem value="moderate">Moderate</SelectItem>
                  <SelectItem value="aggressive">Aggressive</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Target Annual Return (%)</label>
              <Input
                type="number"
                value={returnTarget}
                onChange={(e) => setReturnTarget(e.target.value)}
                className="bg-background"
              />
            </div>
          </div>
        </div>

        <Button className="w-full h-12 text-base glow-green gap-2" onClick={() => setStep("analysis")}>
          <Sparkles className="h-5 w-5" /> Analyze My Investments
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>

      <Footer />
    </div>
  );
}
