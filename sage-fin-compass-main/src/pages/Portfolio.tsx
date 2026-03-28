import { useState } from "react";
import {
  Briefcase, Upload, Plus, Trash2, TrendingUp, TrendingDown,
  Sparkles, AlertCircle, ArrowUpRight, ArrowDownRight, RefreshCw
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { samplePortfolio, companyStocks, sectorAllocation, type PortfolioStock } from "@/data/dummyData";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

const aiInsights = [
  {
    type: "warning" as const,
    title: "Sector Concentration Risk",
    detail: "Your portfolio has 30% allocation to IT sector. Consider reducing to 20-25% and diversifying into Defense and Pharma sectors for better risk-adjusted returns.",
  },
  {
    type: "suggestion" as const,
    title: "Missing: Defense & Pharma Sectors",
    detail: "You have no exposure to Defense (HAL, BEL) or Pharma (Sun Pharma, Dr. Reddy's). Adding 2-3 stocks from these sectors would improve diversification and hedge against IT sector volatility.",
  },
  {
    type: "positive" as const,
    title: "Good Banking Exposure",
    detail: "Your banking allocation at 25% is well-balanced between private (HDFC Bank) and public (SBI) sector banks. This provides good coverage of the financial sector.",
  },
  {
    type: "timing" as const,
    title: "TCS — Consider Buying on Dip",
    detail: "Based on candlestick pattern analysis, TCS has strong support at ₹3,050-3,100 range. Current price of ₹3,245 is 5% above support. Consider adding 5-10 shares if price drops to ₹3,100 range for better entry. Historical data shows 3 successful bounces from this level in the past 6 months.",
  },
  {
    type: "suggestion" as const,
    title: "Add Infrastructure Exposure",
    detail: "Consider adding L&T (Larsen & Toubro) given India's ₹10 lakh crore infrastructure spending. Suggested allocation: 5-8% of portfolio. Current PE of 33.8 is reasonable given the strong order book growth of 20%+ YoY.",
  },
  {
    type: "risk" as const,
    title: "Volatility Alert: Tata Motors",
    detail: "Tata Motors shows high beta of 1.4. While EV growth story is strong, consider trimming position from 35 to 25 shares to limit downside risk. The stock has corrected 17% from its 52-week high.",
  },
];

export default function PortfolioPage() {
  const [portfolio, setPortfolio] = useState<PortfolioStock[]>(samplePortfolio);
  const [showAnalysis, setShowAnalysis] = useState(true);
  const [showAddStock, setShowAddStock] = useState(false);
  const [newSymbol, setNewSymbol] = useState("");
  const [newQty, setNewQty] = useState("");
  const [uploaded, setUploaded] = useState(true);

  const totalInvested = portfolio.reduce((sum, s) => sum + s.avgPrice * s.quantity, 0);
  const totalCurrent = portfolio.reduce((sum, s) => sum + s.currentPrice * s.quantity, 0);
  const totalPnL = totalCurrent - totalInvested;
  const totalPnLPercent = ((totalPnL / totalInvested) * 100).toFixed(2);

  const sectorData = Object.entries(
    portfolio.reduce((acc, s) => {
      const val = s.currentPrice * s.quantity;
      acc[s.sector] = (acc[s.sector] || 0) + val;
      return acc;
    }, {} as Record<string, number>)
  ).map(([name, value]) => ({ name, value: +((value / totalCurrent) * 100).toFixed(1) }));

  const colors = ["hsl(160,84%,39%)", "hsl(217,91%,60%)", "hsl(38,92%,50%)", "hsl(270,76%,55%)", "hsl(0,72%,51%)", "hsl(160,60%,50%)"];

  const handleAddStock = () => {
    const stock = companyStocks.find((s) => s.symbol === newSymbol.toUpperCase());
    if (!stock || !newQty) return;
    const existing = portfolio.find((p) => p.symbol === stock.symbol);
    if (existing) {
      setPortfolio(
        portfolio.map((p) =>
          p.symbol === stock.symbol
            ? { ...p, quantity: p.quantity + parseInt(newQty), avgPrice: ((p.avgPrice * p.quantity + stock.price * parseInt(newQty)) / (p.quantity + parseInt(newQty))) }
            : p
        )
      );
    } else {
      setPortfolio([...portfolio, {
        symbol: stock.symbol,
        name: stock.name,
        quantity: parseInt(newQty),
        avgPrice: stock.price,
        currentPrice: stock.price,
        sector: stock.sector,
      }]);
    }
    setNewSymbol("");
    setNewQty("");
    setShowAddStock(false);
  };

  const removeStock = (symbol: string) => {
    setPortfolio(portfolio.filter((p) => p.symbol !== symbol));
  };

  if (!uploaded) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <TickerBar />
        <div className="container mx-auto px-4 py-8">
          <h1 className="font-heading text-3xl font-bold flex items-center gap-2 mb-6">
            <Briefcase className="h-8 w-8 text-primary" /> Portfolio Analyzer
          </h1>
          <div className="flex flex-col items-center justify-center py-20">
            <div className="glass-card max-w-lg p-8 text-center">
              <Upload className="mx-auto mb-4 h-12 w-12 text-primary" />
              <h2 className="font-heading text-xl font-semibold">Upload Your Portfolio</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Upload your portfolio as a CSV, PDF, or image to create your dummy portfolio for AI analysis.
              </p>
              <div className="mt-6 space-y-3">
                <div className="flex items-center justify-center rounded-lg border-2 border-dashed border-border p-6 cursor-pointer hover:border-primary/50 transition-colors"
                  onClick={() => setUploaded(true)}
                >
                  <div className="text-center">
                    <Upload className="mx-auto mb-2 h-8 w-8 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">Click to upload CSV, PDF, or Image</p>
                    <p className="text-xs text-muted-foreground mt-1">Supports Zerodha, Groww, Angel One exports</p>
                  </div>
                </div>
                <Button className="w-full glow-green" onClick={() => setUploaded(true)}>
                  Use Sample Portfolio
                </Button>
              </div>
            </div>
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

      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
              <Briefcase className="h-8 w-8 text-primary" /> My Portfolio
            </h1>
            <p className="mt-1 text-muted-foreground">Dummy portfolio — tweak stocks and re-analyze anytime</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowAddStock(!showAddStock)} className="gap-1">
              <Plus className="h-3.5 w-3.5" /> Add Stock
            </Button>
            <Button size="sm" className="gap-1 glow-green" onClick={() => setShowAnalysis(!showAnalysis)}>
              <Sparkles className="h-3.5 w-3.5" /> {showAnalysis ? "Hide" : "Run"} AI Analysis
            </Button>
          </div>
        </div>

        {/* Add Stock */}
        {showAddStock && (
          <div className="glass-card mb-4 p-4 flex gap-3 items-end">
            <div className="flex-1">
              <label className="text-xs text-muted-foreground mb-1 block">Symbol</label>
              <Input
                placeholder="e.g., SUNPHARMA"
                value={newSymbol}
                onChange={(e) => setNewSymbol(e.target.value.toUpperCase())}
                className="bg-background"
              />
            </div>
            <div className="w-32">
              <label className="text-xs text-muted-foreground mb-1 block">Quantity</label>
              <Input
                type="number"
                placeholder="Qty"
                value={newQty}
                onChange={(e) => setNewQty(e.target.value)}
                className="bg-background"
              />
            </div>
            <Button onClick={handleAddStock} className="glow-green">Add</Button>
          </div>
        )}

        {/* Summary Cards */}
        <div className="grid gap-4 sm:grid-cols-4 mb-6">
          <div className="glass-card p-4">
            <span className="text-xs text-muted-foreground">Total Invested</span>
            <div className="font-heading text-xl font-bold mt-1">₹{totalInvested.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
          </div>
          <div className="glass-card p-4">
            <span className="text-xs text-muted-foreground">Current Value</span>
            <div className="font-heading text-xl font-bold mt-1">₹{totalCurrent.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
          </div>
          <div className="glass-card p-4">
            <span className="text-xs text-muted-foreground">P&L</span>
            <div className={`font-heading text-xl font-bold mt-1 flex items-center gap-1 ${totalPnL >= 0 ? "text-primary" : "text-destructive"}`}>
              {totalPnL >= 0 ? <ArrowUpRight className="h-4 w-4" /> : <ArrowDownRight className="h-4 w-4" />}
              ₹{Math.abs(totalPnL).toLocaleString(undefined, { maximumFractionDigits: 0 })}
              <span className="text-sm">({totalPnLPercent}%)</span>
            </div>
          </div>
          <div className="glass-card p-4">
            <span className="text-xs text-muted-foreground">Stocks</span>
            <div className="font-heading text-xl font-bold mt-1">{portfolio.length}</div>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Holdings */}
          <div className="lg:col-span-2 space-y-3">
            <h2 className="font-heading text-lg font-semibold">Holdings</h2>
            <div className="space-y-2">
              {portfolio.map((s) => {
                const pnl = (s.currentPrice - s.avgPrice) * s.quantity;
                const pnlPct = ((s.currentPrice - s.avgPrice) / s.avgPrice * 100).toFixed(2);
                return (
                  <div key={s.symbol} className="glass-card p-4 flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent font-heading text-xs font-bold shrink-0">
                      {s.symbol.slice(0, 2)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-heading text-sm font-semibold">{s.symbol}</span>
                        <Badge variant="outline" className="text-[10px]">{s.sector}</Badge>
                      </div>
                      <span className="text-xs text-muted-foreground">{s.name}</span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm">Qty: <span className="font-medium">{s.quantity}</span></div>
                      <div className="text-xs text-muted-foreground">Avg: ₹{s.avgPrice.toLocaleString()}</div>
                    </div>
                    <div className="text-right min-w-[100px]">
                      <div className="text-sm font-medium">₹{(s.currentPrice * s.quantity).toLocaleString()}</div>
                      <div className={`flex items-center justify-end gap-0.5 text-xs ${pnl >= 0 ? "text-primary" : "text-destructive"}`}>
                        {pnl >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                        {pnl >= 0 ? "+" : ""}₹{Math.abs(pnl).toFixed(0)} ({pnlPct}%)
                      </div>
                    </div>
                    <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0" onClick={() => removeStock(s.symbol)}>
                      <Trash2 className="h-3.5 w-3.5 text-muted-foreground hover:text-destructive" />
                    </Button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Sector Chart */}
          <div>
            <h2 className="font-heading text-lg font-semibold mb-3">Sector Allocation</h2>
            <div className="glass-card p-4">
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie data={sectorData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} innerRadius={50} strokeWidth={0}>
                    {sectorData.map((_, i) => (
                      <Cell key={i} fill={colors[i % colors.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ background: "hsl(222,47%,9%)", border: "1px solid hsl(217,33%,17%)", borderRadius: 8, fontSize: 12 }}
                    formatter={(v: number) => [`${v}%`, "Allocation"]}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-1.5 mt-2">
                {sectorData.map((s, i) => (
                  <div key={s.name} className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className="h-2.5 w-2.5 rounded-full" style={{ background: colors[i % colors.length] }} />
                      <span>{s.name}</span>
                    </div>
                    <span className="font-medium">{s.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* AI Analysis */}
        {showAnalysis && (
          <div className="mt-8">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="h-5 w-5 text-primary" />
              <h2 className="font-heading text-lg font-semibold">AI Portfolio Analysis</h2>
              <Button variant="ghost" size="sm" className="ml-auto gap-1 text-xs">
                <RefreshCw className="h-3 w-3" /> Re-analyze
              </Button>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              {aiInsights.map((insight, i) => (
                <div
                  key={i}
                  className={`glass-card p-4 border-l-4 ${
                    insight.type === "warning" ? "border-l-warning" :
                    insight.type === "positive" ? "border-l-primary" :
                    insight.type === "risk" ? "border-l-destructive" :
                    insight.type === "timing" ? "border-l-chart-blue" :
                    "border-l-chart-purple"
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    {insight.type === "warning" && <AlertCircle className="h-4 w-4 text-warning" />}
                    {insight.type === "positive" && <TrendingUp className="h-4 w-4 text-primary" />}
                    {insight.type === "suggestion" && <Sparkles className="h-4 w-4 text-chart-purple" />}
                    {insight.type === "timing" && <RefreshCw className="h-4 w-4 text-chart-blue" />}
                    {insight.type === "risk" && <AlertCircle className="h-4 w-4 text-destructive" />}
                    <h3 className="font-heading text-sm font-semibold">{insight.title}</h3>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">{insight.detail}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
