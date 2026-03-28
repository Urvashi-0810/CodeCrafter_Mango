import { useState, useRef } from "react";
import {
  Briefcase, Upload, Plus, Trash2, TrendingUp, TrendingDown,
  Sparkles, AlertCircle, ArrowUpRight, ArrowDownRight, RefreshCw, FileText, Loader2,
  BarChart2, AlertTriangle, Zap, Info, CheckCircle, ChevronRight
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { samplePortfolio, companyStocks, sectorAllocation, type PortfolioStock } from "@/data/dummyData";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import { toast } from "sonner";

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

  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'preview' | 'success'>('idle');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [activeTab, setActiveTab] = useState('overview');
  
  const [recommendationsItems, setRecommendationsItems] = useState([
    { id: 1, type: "diversification", title: "Risk Diversification", action: "Add", symbol: "HDFCBANK", shares: 20, reason: "Banking sector exposure for stability", applied: false, impact: "Medium", bg: "bg-yellow-50 dark:bg-yellow-900/10", border: "border-yellow-200 dark:border-yellow-700/50" },
    { id: 2, type: "dividend", title: "Dividend Optimization", action: "Add", symbol: "ITC", shares: 30, reason: "FMCG diversification and dividend income", applied: false, impact: "Medium", bg: "bg-yellow-50 dark:bg-yellow-900/10", border: "border-yellow-200 dark:border-yellow-700/50" },
    { id: 3, type: "rebalance", title: "Portfolio Rebalancing", action: "Reduce", symbol: "INFY", shares: 20, reason: "Trim IT overweight, lock in gains", applied: false, impact: "High", bg: "bg-red-50 dark:bg-red-900/10", border: "border-red-200 dark:border-red-700/50" },
    { id: 4, type: "tax", title: "Tax-Loss Harvesting Opportunity", action: "Monitor", symbol: "None", shares: 0, reason: "No current losses. Your portfolio is performing well.", applied: true, impact: "Low", bg: "bg-green-50 dark:bg-green-900/10", border: "border-green-200 dark:border-green-700/50" },
    { id: 5, type: "growth_2", title: "Real Estate Push", action: "Add", symbol: "DLF", shares: 15, reason: "Real estate sector bet on infrastructure push", applied: false, impact: "Low", bg: "bg-primary/10 dark:bg-primary/10", border: "border-blue-200 dark:border-blue-700/50" }
  ]);

  const applyRecommendation = (rec: any) => {
    if (rec.action === "Monitor") return;
    
    const stockInfo = companyStocks.find(s => s.symbol === rec.symbol);
    const currentPrice = stockInfo ? stockInfo.price : (rec.symbol === 'DLF' ? 850 : 1000);
    const sector = stockInfo ? stockInfo.sector : (rec.symbol === 'DLF' ? 'Real Estate' : 'Other');
    const name = stockInfo ? stockInfo.name : rec.symbol;

    if (rec.action === "Add") {
      const existing = portfolio.find(p => p.symbol === rec.symbol);
      let newPortfolio = [...portfolio];
      if (existing) {
        newPortfolio = newPortfolio.map(p => p.symbol === rec.symbol 
          ? { ...p, quantity: p.quantity + rec.shares, avgPrice: ((p.avgPrice * p.quantity) + (currentPrice * rec.shares))/(p.quantity + rec.shares) }
          : p
        );
      } else {
        newPortfolio.push({
          symbol: rec.symbol,
          name: name,
          quantity: rec.shares,
          avgPrice: currentPrice * 0.98,
          currentPrice: currentPrice,
          sector: sector
        });
      }
      setPortfolio(newPortfolio);
      toast.success(`Successfully added ${rec.shares} shares of ${rec.symbol}`);
    } else if (rec.action === "Reduce") {
      const existing = portfolio.find(p => p.symbol === rec.symbol);
      if (existing) {
        if (existing.quantity <= rec.shares) {
          setPortfolio(portfolio.filter(p => p.symbol !== rec.symbol));
        } else {
          setPortfolio(portfolio.map(p => p.symbol === rec.symbol 
            ? { ...p, quantity: p.quantity - rec.shares }
            : p
          ));
        }
        toast.success(`Successfully reduced ${rec.shares} shares of ${rec.symbol}`);
      }
    }

    setRecommendationsItems(recommendationsItems.map(r => r.id === rec.id ? { ...r, applied: true } : r));
  };


  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadState('uploading');
      // Simulate file reading delay
      setTimeout(() => {
        setUploadedFile(file);
        setUploadState('preview');
      }, 1500);
    }
  };

  const confirmImport = () => {
    toast.success(`${uploadedFile?.name} imported successfully!`);
    setUploadState('success');
    
    // Auto-reset UI after 3 seconds
    setTimeout(() => {
      setUploadState('idle');
      setUploadedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }, 3000);
  };

  const cancelImport = () => {
    setUploadState('idle');
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

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

  const sortedSectors = [...sectorData].sort((a,b) => b.value - a.value);
  const topSector = sortedSectors[0];
  const isConcentrated = topSector && topSector.value > 30;
  const hasDefensive = portfolio.some(p => p.sector === 'Banking' || p.sector === 'FMCG');


  const handleAddStock = () => {
    if (!newSymbol || !newQty) return;

    const symbolUpper = newSymbol.toUpperCase();
    const stockMatch = companyStocks.find((s) => s.symbol === symbolUpper);

    const existing = portfolio.find((p) => p.symbol === symbolUpper);
    const priceToUse = stockMatch ? stockMatch.price : 1050; // Random mock price if not found
    const sectorToUse = stockMatch ? stockMatch.sector : "Other";
    const nameToUse = stockMatch ? stockMatch.name : symbolUpper;

    if (existing) {
      setPortfolio(
        portfolio.map((p) =>
          p.symbol === symbolUpper
            ? { ...p, quantity: p.quantity + parseInt(newQty), avgPrice: ((p.avgPrice * p.quantity + priceToUse * parseInt(newQty)) / (p.quantity + parseInt(newQty))) }
            : p
        )
      );
    } else {
      setPortfolio([...portfolio, {
        symbol: symbolUpper,
        name: nameToUse,
        quantity: parseInt(newQty),
        avgPrice: priceToUse * 0.95, // Mock slightly lower buy price
        currentPrice: priceToUse,
        sector: sectorToUse,
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
            <Button size="sm" className="gap-1 glow-green" onClick={() => setShowAnalysis(!showAnalysis)}>
              <Sparkles className="h-3.5 w-3.5" /> {showAnalysis ? "Hide" : "Run"} AI Analysis
            </Button>
          </div>
        </div>

        {/* Import Portfolio Section */}
        {uploadState === 'idle' && (
          <div className="mb-6 flex flex-col sm:flex-row items-center justify-between rounded-xl border border-primary/20 bg-primary/5 p-5 shadow-sm dark:border-primary/40 dark:bg-blue-950/20">
            <div className="flex items-center gap-4 w-full">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary/20 text-primary dark:bg-primary/50 dark:text-primary">
                <Upload className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <h3 className="font-heading text-base font-bold text-slate-800 dark:text-slate-200">Import Your Portfolio</h3>
                <p className="text-[13px] font-medium text-slate-500 dark:text-slate-400 mt-1">Upload CSV, PDF, or screenshot of your holdings</p>
              </div>
            </div>
            <div className="mt-4 sm:mt-0 w-full sm:w-auto shrink-0">
              <input 
                type="file" 
                className="hidden" 
                ref={fileInputRef} 
                onChange={handleFileUpload}
                accept=".csv,.pdf,image/*" 
              />
              <Button 
                onClick={() => fileInputRef.current?.click()}
                className="w-full sm:w-auto bg-primary text-white hover:bg-primary/90 h-10 px-6 rounded-md font-medium shadow-sm transition-colors"
              >
                Choose File
              </Button>
            </div>
          </div>
        )}

        {uploadState === 'uploading' && (
          <div className="mb-6 flex items-center justify-center rounded-xl border border-primary/20 bg-primary/5 p-8 shadow-sm dark:border-primary/40 dark:bg-blue-950/20">
            <div className="flex flex-col items-center gap-3">
              <Loader2 className="h-8 w-8 text-primary animate-spin" />
              <p className="text-sm font-medium text-slate-600 dark:text-slate-300">Reading your file...</p>
            </div>
          </div>
        )}

        {uploadState === 'preview' && uploadedFile && (
          <div className="mb-6 flex flex-col sm:flex-row items-center justify-between rounded-xl border border-primary/20 bg-primary/5 p-5 shadow-sm dark:border-primary/40 dark:bg-blue-950/20">
            <div className="flex items-center gap-4 w-full">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary/20 text-primary dark:bg-primary/50 dark:text-primary">
                <FileText className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <h3 className="font-heading text-base font-bold text-slate-800 dark:text-slate-200">File Ready for Import</h3>
                <p className="text-[13px] font-medium text-slate-500 dark:text-slate-400 mt-1 whitespace-nowrap overflow-hidden text-ellipsis max-w-[200px] sm:max-w-xs cursor-default" title={uploadedFile.name}>
                  {uploadedFile.name} ({(uploadedFile.size / 1024).toFixed(1)} KB)
                </p>
              </div>
            </div>
            <div className="mt-4 sm:mt-0 w-full sm:w-auto flex shrink-0 gap-3">
              <Button variant="outline" className="h-10 px-6 font-medium rounded-md" onClick={cancelImport}>Cancel</Button>
              <Button className="bg-primary hover:bg-primary/90 text-white h-10 px-6 font-medium rounded-md" onClick={confirmImport}>Confirm Import</Button>
            </div>
          </div>
        )}

        {uploadState === 'success' && (
          <div className="mb-6 flex items-center justify-center rounded-xl border border-green-200 bg-green-50/50 p-6 shadow-sm dark:border-green-900/40 dark:bg-green-950/20 animate-in fade-in zoom-in duration-300">
            <div className="flex flex-col items-center gap-2 text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-900/50 dark:text-green-400 shadow-sm border border-green-200/50">
                <svg className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div className="mt-1">
                <h3 className="font-heading text-lg font-bold text-slate-800 dark:text-slate-200">Successfully Uploaded!</h3>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mt-1">Your portfolio insights have been updated.</p>
              </div>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="flex border-b mb-6 gap-6 w-full overflow-x-auto hide-scrollbar">
          {['Overview', 'Analysis', 'Recommendations'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab.toLowerCase())}
              className={`py-2 text-sm font-semibold transition-colors border-b-2 whitespace-nowrap ${
                activeTab === tab.toLowerCase() 
                ? 'border-primary text-primary dark:text-primary dark:border-primary/50' 
                : 'border-transparent text-muted-foreground hover:text-foreground hover:border-muted'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === 'overview' && (
          <div className="space-y-6 animate-in fade-in duration-300">
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

                {/* Add Stock Button & Form */}
                {!showAddStock && (
                  <Button
                    variant="outline"
                    className="w-full mt-4 border-dashed border-2 py-6 text-muted-foreground hover:text-foreground hover:bg-accent/50 gap-2"
                    onClick={() => setShowAddStock(true)}
                  >
                    <Plus className="h-5 w-5" /> Add Stock
                  </Button>
                )}

                {showAddStock && (
                  <div className="glass-card mt-4 p-4 flex gap-3 items-end border border-primary/20 bg-background/50 shadow-sm relative">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute -top-3 -right-3 h-6 w-6 rounded-full bg-background border shadow-sm hover:bg-destructive hover:text-destructive-foreground z-10"
                      onClick={() => setShowAddStock(false)}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                    <div className="flex-[3]">
                      <label className="text-xs text-muted-foreground font-medium mb-1.5 block">Symbol</label>
                      <Input
                        placeholder="e.g., SUNPHARMA"
                        value={newSymbol}
                        onChange={(e) => setNewSymbol(e.target.value.toUpperCase())}
                        className="bg-background h-10 w-full"
                      />
                    </div>
                    <div className="flex-1 min-w-[100px]">
                      <label className="text-xs text-muted-foreground font-medium mb-1.5 block">Quantity</label>
                      <Input
                        type="number"
                        placeholder="Qty"
                        value={newQty}
                        onChange={(e) => setNewQty(e.target.value)}
                        className="bg-background h-10 w-full"
                      />
                    </div>
                    <Button onClick={handleAddStock} className="glow-green h-10 px-6 text-sm font-medium">Add</Button>
                  </div>
                )}
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
                        contentStyle={{ background: "hsl(222,47%,9%)", border: "1px solid hsl(217,33%,17%)", borderRadius: 8, fontSize: 12, color: "#fff" }}
                        itemStyle={{ color: "#fff" }}
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
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div className="grid gap-6 md:grid-cols-2">
              <div className="glass-card p-6">
                 <h3 className="font-heading text-lg font-bold flex items-center gap-2 mb-6"><BarChart2 className="h-5 w-5 text-primary"/> Sector Allocation</h3>
                 <div className="space-y-5">
                   {sortedSectors.map(s => (
                     <div key={s.name}>
                       <div className="flex justify-between text-sm mb-2 font-medium">
                         <span className="text-muted-foreground">{s.name}</span>
                         <span className="text-primary font-bold">{s.value}%</span>
                       </div>
                       <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                         <div className="h-full bg-primary transition-all duration-500 rounded-full" style={{ width: `${s.value}%` }} />
                       </div>
                     </div>
                   ))}
                 </div>
              </div>
              <div className="glass-card p-6 relative overflow-hidden">
                 <div className={`absolute top-0 left-0 w-1.5 h-full ${isConcentrated ? 'bg-orange-400' : 'bg-green-400'} transition-colors`}/>
                 <h3 className="font-heading text-lg font-bold flex items-center gap-2 mb-6 ml-2"><AlertTriangle className={`h-5 w-5 ${isConcentrated ? 'text-orange-500' : 'text-green-500'}`}/> Risk Assessment</h3>
                 <div className="space-y-5 ml-2">
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Volatility</p>
                     <p className={`font-semibold text-sm ${hasDefensive ? 'text-green-600 dark:text-green-400' : 'text-slate-800 dark:text-slate-200'}`}>{hasDefensive ? 'Low-Moderate' : 'Moderate-High'}</p>
                   </div>
                   <div className="h-px bg-border/50" />
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Concentration</p>
                     <p className={`font-semibold text-sm flex items-center gap-2 ${isConcentrated ? 'text-orange-600 dark:text-orange-400' : 'text-green-600 dark:text-green-400'}`}>
                       {topSector ? (isConcentrated ? `High ${topSector.name} (${topSector.value}%)` : 'Optimally Balanced') : 'Normal'}
                     </p>
                   </div>
                   <div className="h-px bg-border/50" />
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Diversification Status</p>
                     <p className={`font-semibold text-sm ${isConcentrated ? 'text-orange-600 dark:text-orange-400' : 'text-green-600 dark:text-green-400'}`}>{isConcentrated ? 'Needs Improvement' : 'Excellent'}</p>
                   </div>
                   {isConcentrated ? (
                     <div className="rounded-lg bg-orange-50 dark:bg-orange-900/20 p-4 border border-orange-100 dark:border-orange-500/20">
                       <p className="text-xs text-orange-800 dark:text-orange-300"><span className="font-semibold">AI Recommendation:</span> Add defensive stocks from Banking/FMCG sectors to dilute IT concentration.</p>
                     </div>
                   ) : (
                     <div className="rounded-lg bg-green-50 dark:bg-green-900/20 p-4 border border-green-100 dark:border-green-500/20">
                       <p className="text-xs text-green-800 dark:text-green-300"><span className="font-semibold">AI Status:</span> Portfolio is currently maintaining optimal sector allocation ratios!</p>
                     </div>
                   )}
                 </div>
              </div>
            </div>

            <h3 className="font-heading text-lg font-bold flex items-center gap-2 mt-8 mb-4"><Zap className="h-5 w-5 text-amber-500"/> Investment Strategies & Recommendations</h3>
            <div className="grid gap-4 md:grid-cols-2">
               {recommendationsItems.slice(0,4).map((rec, i) => (
                 <div key={i} className={`p-5 rounded-xl border transition-colors duration-500 ${rec.applied ? 'bg-green-50/50 dark:bg-green-900/10 border-green-200 dark:border-green-900/50' : rec.bg + ' ' + rec.border} dark:bg-background/50`}>
                   <div className="flex justify-between items-start mb-2">
                     <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200 flex items-center gap-2">{rec.title}</h4>
                     <Badge variant="outline" className={`text-[10px] bg-white dark:bg-slate-900 ${rec.applied ? 'text-green-600 border-green-200 dark:text-green-400 dark:border-green-900' : (rec.impact === 'High' ? 'text-red-600 border-red-200 dark:text-red-400 dark:border-red-900' : (rec.impact === 'Medium' ? 'text-yellow-600 border-yellow-200 dark:text-yellow-500 dark:border-yellow-900' : 'text-green-600 border-green-200 dark:text-green-400 dark:border-green-900'))}`}>{rec.applied ? 'Resolved ✓' : rec.impact}</Badge>
                   </div>
                   <p className="text-xs text-slate-600 dark:text-slate-400 mb-4 h-8">{rec.applied ? 'This strategic objective has been successfully executed.' : rec.reason}</p>
                   <div className="h-px bg-slate-200/50 dark:bg-slate-700/50 w-full mb-3" />
                   <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Status:</p>
                   <p className={`text-sm font-medium px-3 py-2 rounded-md border ${rec.applied ? 'text-green-700 bg-green-100/50 border-green-200 dark:text-green-400 dark:bg-green-900/20 dark:border-green-800' : 'text-slate-800 dark:text-slate-200 bg-white/50 dark:bg-slate-900/50 border-white dark:border-slate-800'}`}>
                     {rec.applied ? '✓ Monitoring Performance' : (rec.action === 'Monitor' ? rec.reason : `${rec.action} ${rec.symbol} position ${rec.action === 'Add' ? 'by' : 'sell'} ${rec.shares} shares`)}
                   </p>
                 </div>
               ))}
            </div>
            
            <div className="glass-card p-6 mt-6">
               <h3 className="font-heading text-lg font-bold mb-6">Portfolio Analysis Summary</h3>
               <div className="grid gap-8 md:grid-cols-2">
                 <div>
                   <h4 className="text-sm font-bold mb-4 flex items-center gap-2 text-slate-800 dark:text-slate-200"><TrendingUp className="h-4 w-4 text-green-500"/> Strengths</h4>
                   <ul className="space-y-3 text-sm text-muted-foreground">
                     <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Strong overall returns at {totalPnLPercent}% growth</li>
                     <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Diversified across {sectorData.length} core holding sectors</li>
                     {hasDefensive && <li className="flex items-start gap-2 animate-in fade-in duration-500"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Solid defensive backbone limits drawdown risks</li>}
                     {!isConcentrated && <li className="flex items-start gap-2 animate-in fade-in duration-500"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Optimal sector allocation targets successfully met</li>}
                   </ul>
                 </div>
                 <div>
                   <h4 className="text-sm font-bold mb-4 flex items-center gap-2 text-slate-800 dark:text-slate-200"><TrendingDown className="h-4 w-4 text-orange-500"/> Areas to Improve</h4>
                   <ul className="space-y-3 text-sm text-muted-foreground">
                     {isConcentrated && <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Tech sector concentration risks need monitoring</li>}
                     {!hasDefensive && <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Consider adding defensive stocks for volatility protection</li>}
                     {(!isConcentrated && hasDefensive) ? (
                         <li className="flex items-start gap-2 text-green-600 dark:text-green-400 font-medium animate-in fade-in duration-500"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> All major structural portfolio risks mitigated!</li>
                     ) : (
                         <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Regular rebalancing schedule should be established</li>
                     )}
                   </ul>
                 </div>
               </div>
            </div>

            <div className="bg-primary/10 dark:bg-primary/10 border border-primary/20 dark:border-primary/30 rounded-xl p-6 mt-6 shadow-sm">
              <h3 className="text-sm font-bold text-slate-800 dark:text-slate-200 mb-4">Next Steps</h3>
              <ol className="list-decimal list-outside ml-4 space-y-2.5 text-sm text-slate-600 dark:text-slate-400 font-medium font-sans">
                {isConcentrated ? <li>Execute recommended rebalancing actions</li> : <li><strike className="text-slate-400">Execute recommended rebalancing actions</strike> <span className="text-green-600 ml-1">✓ Done</span></li>}
                <li>Review quarterly earnings for top sector holdings</li>
                <li>Set up automated dividend reinvestment</li>
                <li>Schedule monthly portfolio review</li>
                <li>Monitor RBI and market regulatory changes</li>
              </ol>
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
             <div className="flex flex-col sm:flex-row items-center sm:items-start gap-4 bg-primary/10 dark:bg-primary/20 border border-primary/20 dark:border-primary/40 rounded-xl p-5 mb-6 shadow-sm">
               <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary text-white">
                 <Zap className="h-5 w-5" />
               </div>
               <div>
                  <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200 text-center sm:text-left">AI-Powered Optimization</h4>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 text-center sm:text-left">Based on your current holdings, we recommend diversifying into defensive sectors and reducing IT concentration.</p>
               </div>
             </div>

             <div className="space-y-3">
               {recommendationsItems.filter(r => r.action !== 'Monitor').map(rec => (
                 <div key={rec.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 hover:shadow-md transition-all">
                    <div className="mb-4 sm:mb-0">
                      <h4 className="font-bold text-[15px] flex items-center gap-2">
                        {rec.action} {rec.symbol} <span className="text-slate-400 font-normal">—</span> 
                        {rec.action === 'Reduce' ? 'sell' : ''} {rec.shares} shares
                      </h4>
                      <p className="text-sm text-muted-foreground mt-1">{rec.reason}</p>
                    </div>
                    <Button 
                      onClick={() => !rec.applied && applyRecommendation(rec)}
                      disabled={rec.applied}
                      className={`shrink-0 w-full sm:w-28 font-semibold ${rec.applied ? 'bg-primary/10 text-primary hover:bg-primary/10 cursor-default border-none dark:bg-primary/20 dark:text-primary' : 'bg-primary/10 text-primary hover:bg-primary/20 dark:bg-primary/40 dark:text-primary'}`}
                      variant="secondary"
                    >
                      {rec.applied ? 'Applied' : 'Apply'}
                    </Button>
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
